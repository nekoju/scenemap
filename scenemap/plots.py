#!/usr/bin/env python3

import networkx as nx
import plotly.express as px

class NetworkGraph:
    def __init__(self, artist_data):
        self.artist_data = artist_data

    def generate_graph(self, draw_attrs=None):
        """
        draw_attrs (list-like): Any of ['current_members', 'former_members', 'associated_acts']
        """
        g = nx.Graph()
        for artist_name, artist_details in self.artist_data.items():
            print(f"adding artist: {artist_name}")
            g.add_node(artist_name, attr_type="artist")
            nodes_to_add = []
            for attribute_name, attribute in artist_details.items():
                if not draw_attrs or attribute in draw_attrs:
                    for name_x in attribute:
                        nodes_to_add.append(name_x)
                        g.add_node(name_x, attr_type=attribute_name)
                        print(f"adding {attribute_name}: {name_x}")
                        g.add_edge(*(artist_name, name_x))
        return g
        

def __main__():
    import matplotlib.pyplot as plt
    import networkx as ng
    from plots import NetworkGraph
    return None
