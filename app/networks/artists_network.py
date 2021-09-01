import matplotlib.pyplot as plt
import networkx as nx

from app.crawler import crawler


def create_network():
    data = {'nodes': {},
            'links': []}
    network = nx.Graph()
    artists = crawler.get_all_artists_followed_by_all_users()
    attr = {}
    print(artists)
    for it in artists.keys():
        artists_array=artists[it]
        for index in range(len(artists_array)):
            for index2 in range(index + 1, len(artists_array)):
                add_edge(network, artists_array[index].id, artists_array[index2].id)
                data['links'].append({'source' : artists_array[index].id, 'target' : artists_array[index2].id})
                data['nodes'][artists_array[index].id] = {'name': artists_array[index].name,
                                          'image': artists_array[index].image,
                                          'genres': artists_array[index].genres,
                                          'related': artists_array[index].related
                                          }
                data['nodes'][artists_array[index2].id] = {'name': artists_array[index2].name,
                                           'image': artists_array[index2].image,
                                           'genres': artists_array[index2].genres,
                                           'related': artists_array[index2].related
                                           }

    #nx.set_node_attributes(network, data)

    return {'graph' : network, 'data' : data}


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


#n = create_network()['graph']
#nx.draw_networkx(n)
#plt.show()