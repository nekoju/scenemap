#!/usr/bin/env python3

import os 

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Notes
# I have no idea if this works. Currently not opening a browser window.
class Spot:
    def __init__(self):
        load_dotenv()
        client_secret = os.getenv("client_secret")
        client_id = os.getenv("client_id")
        redirect_uri = os.getenv("redirect_uri")
        scope = "user-library-read user-read-playback-state user-read-recently-played"
        self.session = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                open_browser=True,
            )
        )
        return None


def main():
    session = Spot()


if __name__ == "__main__":
    main()
