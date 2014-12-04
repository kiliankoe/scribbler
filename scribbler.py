#! /usr/bin/env python3

import requests
import hashlib
import json
import time

def get_token():
	# auth.getToken (GET http://ws.audioscrobbler.com/2.0/)
	api_sig = 'api_key' + api_key + 'methodauth.gettoken' + api_secret
	api_sig = hashlib.md5(api_sig.encode('utf-8')).hexdigest()
	try:
		r = requests.get(
			url="http://ws.audioscrobbler.com/2.0/",
			params = {
				"method":"auth.gettoken",
				"api_sig":api_sig,
				"api_key":api_key,
				"format":"json",
			},
		)
		if r.status_code == 200:
			response = json.loads(r.content.decode())
			return response['token']
	except requests.exceptions.RequestException as e:
		print('Failed to request token.')

def authenticate_user(token):
	# wait for the user to identify with last.fm
	url = 'http://www.last.fm/api/auth/?api_key=' + api_key + '&token=' + token
	print(url)
	input('Please visit the URL, click the button and press Enter when done.\n')

def get_session(token):
	# auth.getSession (GET http://ws.audioscrobbler.com/2.0/)
	api_sig = 'api_key' + api_key + 'methodauth.getSessiontoken' + token + api_secret
	api_sig = hashlib.md5(api_sig.encode('utf-8')).hexdigest()
	try:
		r = requests.get(
			url="http://ws.audioscrobbler.com/2.0/",
			params = {
				"method":"auth.getSession",
				"token":token,
				"api_sig":api_sig,
				"api_key":api_key,
				"format":"json",
			},
		)
		if r.status_code == 200:
			response = json.loads(r.content.decode())
			return response['session']['key']
	except requests.exceptions.RequestException as e:
		print('Failed to request session.')

def post_scrobble(sk, timestamp, artist, track):
	# track.scrobble (POST http://ws.audioscrobbler.com/2.0/)
	api_sig = 'api_key' + api_key + 'artist' + artist + 'methodtrack.scrobblesk' + sk + 'timestamp' + str(timestamp) + 'track' + track + api_secret
	api_sig = hashlib.md5(api_sig.encode('utf-8')).hexdigest()
	try:
		r = requests.post(
			url="http://ws.audioscrobbler.com/2.0/",
			data = {
				"method":"track.scrobble",
				"sk":sk,
				"artist":artist,
				"track":track,
				"timestamp":timestamp,
				"api_sig":api_sig,
				"api_key":api_key,
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



# read secrets
file = open('secrets.txt', 'r')
secrets = file.read().splitlines()
file.close()
api_key = secrets[0]
api_secret = secrets[1]

token = get_token()
authenticate_user(token)
sk = get_session(token)

file = open('scrobble.txt', 'r')
lines = file.readlines()
file.close()

file = open('scrobble.txt', 'w')
for line in lines:
	split_track = line.split(' - ')
	track = split_track[0]
	artist = split_track[1]

	timestamp = int(time.time())
	if post_scrobble(sk, timestamp, artist, track):
		time.sleep(180)
	else:
		file.write(line)
file.close()

print('All done')
