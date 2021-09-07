import random

import networkx as nx
import app.networks.artists_network
from app.crawler import crawler


def artist_recommender(token):
    # Dagli artisti che seguo prendo quelli direttamente collegati con maggiore peso

    current_user = crawler.get_user_info(token)
    user = crawler.db_user(current_user['id'])
    artists_followed = user['artists_followed']
    network = app.networks.artists_network.create_network()['graph']
    small = set()
    medium = set()
    high = set()
    for artist in artists_followed:
        neighbors = network[artist]
        for neighbor in neighbors.keys():
            if neighbors[neighbor]['weight'] == 1:
                small.add(neighbor)
            elif 1 < neighbors[neighbor]['weight'] <= 3:
                medium.add(neighbor)
            else:
                high.add(neighbor)
    artists_weighted = {'small': small, 'medium': medium, 'high': high}
    return artists_weighted


def followship_recommendations(token):
    current_user = crawler.get_user_info(token)
    user = crawler.db_user(current_user['id'])
    users_followed = user['users_followed']
    artists_followed = user['artists_followed']

    weights = {}
    total_weight = 0
    common_artists = {}
    for u in users_followed:
        ca = []
        for x in crawler.db_user(u)['artists_followed']:
            if x in artists_followed:
                try:
                    weights[u] = weights[u] + 1
                    total_weight += 1
                except KeyError:
                    weights[u] = 1
                    total_weight += 1
            else:
                ca.append(x)
        common_artists[u] = ca


    # Nella selezione vado a dare un peso agli utenti che hanno più artisti in comune con me
    # Normalizzo i pesi

    ret_val = []
    for x in weights.keys():
        to_take = int(weights[x] / total_weight * 20)
        e = common_artists[x]
        while to_take > 0:
            artist = random.sample(e, 1)[0]
            e.remove(artist)
            if artist not in ret_val:
                ret_val.append(artist)
                to_take -= 1

    return create_info(ret_val)


def create_info(artists_id):
    ret_val = {}
    for artist in artists_id:
        info = crawler.db_get_artist_by_id(artist).get_as_dict()
        ret_val[info['_id']] = info

    return ret_val