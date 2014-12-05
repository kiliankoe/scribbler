#! /usr/bin/env python3

import requests
import hashlib
import json
import time

class Scribbler:

    api_key = 'not defined'
    api_secret = 'not defined'
    sessionkey = 'not defined'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_token(self):
        # auth.getToken (GET http://ws.audioscrobbler.com/2.0/)
        api_sig = 'api_key' + self.api_key + 'methodauth.gettoken' + self.api_secret
        api_sig = hashlib.md5(api_sig.encode('utf-8')).hexdigest()
        try:
            r = requests.get(
                url="http://ws.audioscrobbler.com/2.0/",
                params = {
                    "method":"auth.gettoken",
                    "api_sig":api_sig,
                    "api_key":self.api_key,
                    "format":"json",
                },
            )
            if r.status_code == 200:
                response = json.loads(r.content.decode())
                return response['token']
        except requests.exceptions.RequestException as e:
            print('Failed to request token.')

    def authenticate_user(self, token):
        # wait for the user to identify with last.fm
        url = 'http://www.last.fm/api/auth/?api_key=' + self.api_key + '&token=' + token
        print(url)
        input('Please visit the URL, click the button and press Enter when done.\n')

    def get_session(self, token):
        # auth.getSession (GET http://ws.audioscrobbler.com/2.0/)
        api_sig = 'api_key' + self.api_key + 'methodauth.getSessiontoken' + token + self.api_secret
        api_sig = hashlib.md5(api_sig.encode('utf-8')).hexdigest()
        try:
            r = requests.get(
                url="http://ws.audioscrobbler.com/2.0/",
                params = {
                    "method":"auth.getSession",
                    "token":token,
                    "api_sig":api_sig,
                    "api_key":self.api_key,
                    "format":"json",
                },
            )
            if r.status_code == 200:
                response = json.loads(r.content.decode())
                return response['session']['key']
        except requests.exceptions.RequestException as e:
            print('Failed to request session.')

    def scrobble(self, timestamp, artist, track):
        # track.scrobble (POST http://ws.audioscrobbler.com/2.0/)
        api_sig = 'api_key' + self.api_key + 'artist' + artist + 'methodtrack.scrobblesk' + self.sessionkey + 'timestamp' + str(timestamp) + 'track' + track + self.api_secret
        api_sig = hashlib.md5(api_sig.encode('utf-8')).hexdigest()
        try:
            r = requests.post(
                url="http://ws.audioscrobbler.com/2.0/",
                data = {
                    "method":"track.scrobble",
                    "sk":self.sessionkey,
                    "artist":artist,
                    "track":track,
                    "timestamp":timestamp,
                    "api_sig":api_sig,
                    "api_key":self.api_key,
                    "format":"json",
                },
            )
            if r.status_code == 200:
                response = json.loads(r.content.decode())
                print(response['scrobbles']['scrobble']['timestamp'] + ' - Scrobbled ' + response['scrobbles']['scrobble']['track']['#text'] + ' by ' + response['scrobbles']['scrobble']['artist']['#text'])
                return True
            else:
                print('Failed to scrobble ' + track + ' by ' + artist)
                return False
        except requests.exceptions.RequestException as e:
            print('Failed to send scrobble request.')

    def authenticate(self):
        token = self.get_token()
        self.authenticate_user(token)
        self.sessionkey = self.get_session(token)
