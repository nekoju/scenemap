#!/usr/bin/env python3

import os 
import requests
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spot:
    """
        Primary spotify object.
    """
    def __init__(self):
        self.artists = {}
        self.albums = {}

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

    def _get_artists(self):
        """
            Parse Spotify API JSON into a dict of artists.
            This will instantiate an empty dict of dicts with artists in the user's
            Spotify saved albums as `self.artists`.
        """
        if not self.albums:
            print("No albums yet. Getting albums.")
            self.get_albums()
        for album in self.albums:
            for artist in album["album"]["artists"]:
                self.artists[artist["name"].strip("'").strip('"')] = {}
        return self.artists

    def get_albums(self, *args, **kwargs):
        """
            Get all user albums. (Raw Spotify output)
        """
        # Handle kwarg defaults
        try:
            limit = kwargs["limit"]
        except KeyError:
            limit = 50
        out = self.session.current_user_saved_albums(limit=limit)
        self.albums = out["items"]
        while out["next"]:
            out = self.session.next(out)
            self.albums.extend(out["items"])
        return self.albums

    @staticmethod
    def get_artist_details(artist_name):
        url = f"https://en.wikipedia.org/wiki/{artist_name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        artist_details = {
            'current_members': [],
            'former_members': [],
            'associated_acts': []
        }

        # Scrape current members
        current_members_section = soup.find('th', text='Members')
        if current_members_section:
            for sibling in current_members_section.find_next_siblings('td'):
                links = sibling.find_all('a')
                for link in links:
                    artist_details['current_members'].append(link.text)

        # Scrape former members
        former_members_section = soup.find('th', text='Past members')
        if former_members_section:
            for sibling in former_members_section.find_next_siblings('td'):
                links = sibling.find_all('a')
                for link in links:
                    artist_details['former_members'].append(link.text)

        # Scrape associated acts
        associated_acts_section = soup.find('th', text='Associated acts')
        if associated_acts_section:
            for sibling in associated_acts_section.find_next_siblings('td'):
                links = sibling.find_all('a')
                for link in links:
                    artist_details['associated_acts'].append(link.text)

        return artist_details

def main():
    session = Spot()
    artists = session._get_artists()
    breakpoint()


if __name__ == "__main__":
    main()
