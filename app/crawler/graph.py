import networkx as nx
from .crawler import *


def create_graph(max_nodes: int, name: str, max_diameter: int = None) -> dict:
    global rel
    if max_diameter is None:
        max_diameter = 4
    g = nx.Graph()

    start = api_get_id(name)
    data = {'nodes': {},
            'links': [],
            'id': start}
    to_link = [start]
    inserted = []
    global y
    while len(to_link) > 0 and len(inserted) <= max_nodes:
        actual = to_link.pop(0)
        art = get_artist_by_id(actual)
        if actual not in inserted:
            g.add_node(actual)
            inserted.append(actual)
            data['nodes'][actual] = {'name': art.get_name(), 'genres': art.get_genres(), 'image': art.get_image()}
        for y in art.get_related():
            if y not in inserted:
                rel = get_artist_by_id(y)
                g.add_node(y)
                inserted.append(y)
                data['nodes'][y] = {'name': rel.get_name(), 'genres': rel.get_genres(), 'image': rel.get_image()}
                to_link.append(y)
            if not g.has_edge(y, actual):
                g.add_edge(actual, y)
                if shortest_path(g, start, y) > max_diameter:

                    #calcolo i path
                    for node in g.nodes:
                        path = shortest_path(g, start, node)
                        data['nodes'][node]['path'] = path
                    g.remove_edge(actual, y)
                    return {'graph': g, 'data': data}
                data['links'].append({'source': actual, 'target': y})

    for node in g.nodes:
        path = shortest_path(g, start, node)
        data['nodes'][node]['path'] = path
    # TODO vedere se serve g come ritorno
    return {'graph': g, 'data': data}


def shortest_path(g: nx.Graph, start, end) -> int:
    path = nx.shortest_path_length(g, start, end)
    return path


