## scribbler

Quick and dirty scrobbling to the last.fm API. For those moments where you can't scrobble right from your player but don't want to not have the tracks show up in your history.

#### Getting started

1. [Register](http://www.lastfm.de/api/account/create) for the Last.fm API and create an application.

2. Install `requests` through pip
    ```sh
    $ pip install requests
    ```

3. Use scribbler

    ```python
    from scribbler import *

    scribbler = Scribbler(api_key, api_secret)
    scribbler.authenticate()
    # Calling authenticate() will prompt you for a URL to visit

    timestamp = int(time.time())
    scribbler.scrobble(timestamp, 'The Glitch Mob', 'We Can Make The World Stop')
    ```

Or use `run.py` for a quick and dirty way of scrobbling a text file of tracks. Be sure to include your api_key and api_secret in a file called `secrets.txt`.
