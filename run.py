#! /usr/bin/env python3

from scribbler import *

# read secrets
file = open('secrets.txt', 'r')
secrets = file.read().splitlines()
file.close()
api_key = secrets[0]
api_secret = secrets[1]

sc = Scribbler(api_key, api_secret)
sc.authenticate()

file = open('scrobble.txt', 'r')
lines = file.readlines()
file.close()

for line in lines:
    split_track = line.split(' - ')
    track = split_track[0]
    artist = split_track[1]

    timestamp = int(time.time())
    if sc.scrobble(timestamp, artist, track):
        time.sleep(180)

print('All done')
