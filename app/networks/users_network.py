import matplotlib.pyplot as plt
import networkx as nx

from app.crawler import crawler
from app.crawler.beans.user_info import User_Info
from app.networks.artists_network import add_edge


def create_network():
    data = {'nodes': {},
            'links': []}
    network = nx.DiGraph()
    users = crawler.user_info()
    attr = {}
    print(users)
    for user in users:
        for index in range(len(user['users_followed'])):
            add_edge(network, user['id'], user['users_followed'][index])
            data['links'].append({'source': user['id'], 'target': user['users_followed'][index]})
            data['nodes'][user['id']] = {'name': user['name'],
                                                          'image': user['image']
                                                          }
    # nx.set_node_attributes(network, data)
    return {'graph': network, 'data': data}

