#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import secrets


# Notes
# I have no idea if this works. Currently not opening a browser window.
class Spot:
    def __init__(self):
        client_secret = secrets.client_secret
        client_id = secrets.client_id
        redirect_uri = "http://localhost:8000"
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
