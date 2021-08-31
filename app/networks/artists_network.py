import matplotlib.pyplot as plt
import networkx as nx

from app.crawler import crawler


def create_network():
    data = {'nodes': {},
            'links': []}
    network = nx.Graph()
    artists = crawler.get_all_artists_followed_by_all_users()
    attr = {}
    for artist in artists:
        for index in range(len(artist)):
            for index2 in range(index + 1, len(artist)):
                add_edge(network, artist[index].id, artist[index2].id)
                attr[artist[index].id] = {'name': artist[index].name,
                                          'image': artist[index].image,
                                          'genres': artist[index].genres,
                                          'related': artist[index].related
                                          }
                attr[artist[index2].id] = {'name': artist[index2].name,
                                           'image': artist[index2].image,
                                           'genres': artist[index2].genres,
                                           'related': artist[index2].related
                                           }

    nx.set_node_attributes(network, attr)
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


n = create_network()
nx.draw_networkx(n)
plt.show()