#!/usr/bin/env python3

import itertools as it
import os
import re
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
        if artist_name == "Starflyer 59":
            breakpoint()
        url = Spot.search(artist_name)
        print(url)
        artist_details = {
            "current_members": [],
            "former_members": [],
            "associated_acts": [],
        }
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.MissingSchema:
            print(f"No meta results for {artist_name}")
            return artist_details

        # Scrape current members
        current_members_regex = re.compile(r"^(Current )?Members")
        current_members_section = soup.find("th", text=current_members_regex)
        if current_members_section:
            for sibling in current_members_section.find_next_siblings("td"):
                links = sibling.get_text().split("\n")
                for link in links:
                    artist_details["current_members"].append(link)

        # Scrape former members
        former_members_section = soup.find("th", text="Past members")
        if former_members_section:
            for sibling in former_members_section.find_next_siblings("td"):
                # Firugre out how to wrk with list items here.
                links = sibling.get_text().split("\n")
                for link in links:
                    artist_details["former_members"].append(link)

        # Scrape associated acts
        associated_acts_section = soup.find("th", text="Associated acts")
        if associated_acts_section:
            for sibling in associated_acts_section.find_next_siblings("td"):
                links = sibling.get_text().split("\n")
                for link in links:
                    artist_details["associated_acts"].append(link)

        print(f"{artist_name}: done")
        return artist_details

    @staticmethod
    def search(query):
        descriptors = [
            "band",
            "musician",
            "songwriter",
            "rapper",
            "artist",
            "composer",
        ]
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
            "srsearch": query + " band",
        }
        response = requests.get(url, params=params).json()["query"]["search"]
        for entry in response:
            for descriptor in descriptors:
                if (
                    descriptor in entry["snippet"].lower()
                    or descriptor in entry["title"].lower()
                ):
                    return f"https://en.wikipedia.org/?curid={entry['pageid']}"


def main():
    import matplotlib.pyplot as plt
    import networkx as nx
    from plots import NetworkGraph
    import pickle

    session = Spot()
    artists = session._get_artists()

    for artist in artists:
        artists[artist] = session.get_artist_details(artist)
    with open("out.pickle", "wb") as file:
        pickle.dump(artists, file)

    # with open("out.pickle", "rb") as file:
    #     pickle.load(file)

    artists_sparse = {}
    for artist_name, artist_attr in artists.items():
        if list(it.chain(artist_attr.values())):
            artists_sparse[artist_name] = artist_attr

    ng = NetworkGraph(artists_sparse)
    g = ng.generate_graph()
    colors = {
        "artist": "black",
        "associated_acts": "blue",
        "former_members": "red",
        "current_members": "green",
    }
    colors_list = []
    for node in g.nodes:
        colors_list.append(colors[g.nodes[node]["attr_type"]])

    nx.draw_networkx(g, node_color=colors_list)
    breakpoint()


if __name__ == "__main__":
    main()
