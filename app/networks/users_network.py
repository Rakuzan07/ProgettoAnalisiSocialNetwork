import matplotlib.pyplot as plt
import networkx as nx

from app.crawler import crawler


def create_network():
    network = nx.DiGraph()
    query = crawler.get_all_users_followed_by_all_users()

    for e in query:
        user = e['id']
        for j in e['users_followed']:
            network.add_edge(user, j)

    return network

network = create_network()
nx.draw_networkx(network)
plt.show()