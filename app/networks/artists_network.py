import matplotlib.pyplot as plt
import networkx as nx

from app.crawler import crawler


def create_network():
    network = nx.Graph()
    artists = crawler.get_all_artists_followed_by_all_users()
    for e in artists:
        for index in range(len(e['artists_followed'])):
            for index2 in range(index + 1, len(e['artists_followed'])):
                add_edge(network, e['artists_followed'][index], e['artists_followed'][index2])
    return network


def add_edge(network: nx.Graph, node1, node2):
    if network.has_edge(node1, node2):
        weight = network.get_edge_data(node1, node2)['weight']
        network.remove_edge(node1, node2)
        network.add_edge(node1, node2, weight=weight + 1)
    else:
        network.add_edge(node1, node2, weight=1)


def draw_network(network: nx.Graph):
    nx.draw_networkx(network)


# TODO: analisi da fare sulla rete degli artisti/utenti
# TODO: costruire rete degli utenti
# TODO: Gestire parte grafica
# TODO: Recommender system