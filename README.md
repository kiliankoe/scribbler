## scribbler

Scrobble a text file of tracks to Last.fm.

#### Getting started

1. [Register](http://www.lastfm.de/api/account/create) for the Last.fm API and create an application.

1. Save your API key and secret to a file called `secrets.txt`
```
api_key
api_secret
```

1. Install `requests` through pip
```sh
$ pip install requests
```

1. Create a file called `scrobble.txt` and fill it with the songs to scrobble.
```
We Can Make The World Stop - The Glitch Mob
Radioactive - Imagine Dragons
```

1. Run scribbler
```
./scribbler.py
```
