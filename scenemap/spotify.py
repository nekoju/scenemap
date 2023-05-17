#!/usr/bin/env python3

import os 
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spot:
    """
        Primary spotify object.
    """
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

    def get_albums(self, *args, **kwargs):
        """
            Get all user albums.
        """
        # Handle kwarg defaults
        try:
            limit = kwargs["limit"]
        except KeyError:
            limit = 50
        breakpoint()
        out = self.session.current_user_saved_albums(limit=limit)
        albums = out["items"]
        while out["next"]:
            out = self.session.next(out)
            albums.extend(out["items"])
        return albums



def main():
    session = Spot()


if __name__ == "__main__":
    main()
