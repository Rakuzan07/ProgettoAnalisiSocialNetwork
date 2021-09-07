import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean
from app.networks import artists_network

plt.style.use("seaborn")

def degree_centrality(G):

    d_centrality=nx.degree_centrality(G)
    centralities = list(d_centrality.values())
    max_centrality = max(centralities)
    min_centrality  = min(centralities)
    avg_centrality = mean(centralities)
    node_max = None
    node_min = None
    for key,value in d_centrality.items():
        if value == max_centrality:
            node_max=key
        if value == min_centrality:
            node_min=key
        if node_max is not None and node_min is not None:
            break
    print(f'Il nodo con centralità massima è {node_max} con valore di degree cenrtality pari a {max_centrality}')
    print(f'Il nodo con centralità minima è {node_min} con valore di degree cenrtality pari a {min_centrality}')
    print(f'La media della degree centrality dei nodi è {avg_centrality}')
    plt.hist(centralities)
    plt.show()


def betweenness_centrality(G):
    d_centrality = nx.betweenness_centrality(G)
    centralities = list(d_centrality.values())
    max_centrality = max(centralities)
    min_centrality = min(centralities)
    avg_centrality = mean(centralities)
    node_max = None
    node_min = None
    for key, value in d_centrality.items():
        if value == max_centrality:
            node_max = key
        if value == min_centrality:
            node_min = key
        if node_max is not None and node_min is not None:
            break
    print(f'Il nodo con centralità massima è {node_max} con valore di betweenness cenrtality pari a {max_centrality}')
    print(f'Il nodo con centralità minima è {node_min} con valore di betweenness cenrtality pari a {min_centrality}')
    print(f'La media della betweenness centrality dei nodi è {avg_centrality}')
    plt.hist(centralities)
    plt.show()

def closeness_centrality(G):
    d_centrality = nx.closeness_centrality(G)
    centralities = list(d_centrality.values())
    max_centrality = max(centralities)
    min_centrality = min(centralities)
    avg_centrality = mean(centralities)
    node_max = None
    node_min = None
    for key, value in d_centrality.items():
        if value == max_centrality:
            node_max = key
        if value == min_centrality:
            node_min = key
        if node_max is not None and node_min is not None:
            break
    print(f'Il nodo con centralità massima è {node_max} con valore di closeness cenrtality pari a {max_centrality}')
    print(f'Il nodo con centralità minima è {node_min} con valore di closeness cenrtality pari a {min_centrality}')
    print(f'La media della closeness centrality dei nodi è {avg_centrality}')
    plt.hist(centralities)
    plt.show()

#def rank():

#def weak_strong_ties():

def eigenvector_analysis(G):
    d_centrality = nx.eigenvector_centrality(G,weight='weight')
    centralities = list(d_centrality.values())
    max_centrality = max(centralities)
    min_centrality = min(centralities)
    avg_centrality = mean(centralities)
    node_max = None
    node_min = None
    for key, value in d_centrality.items():
        if value == max_centrality:
            node_max = key
        if value == min_centrality:
            node_min = key
        if node_max is not None and node_min is not None:
            break
    print(f'Il nodo con centralità massima è {node_max} con valore di eigenvector cenrtality pari a {max_centrality}')
    print(f'Il nodo con centralità minima è {node_min} con valore di eigenvector cenrtality pari a {min_centrality}')
    print(f'La media della eigenvector centrality dei nodi è {avg_centrality}')
    plt.hist(centralities)
    plt.show()

def bridge(G):
    print(f"Il grafo ha i seguenti bridge tra i nodi {list(nx.bridges(G))}")


def modelling(G): # DATO UN GRAFO VOGLIAMO OTTENERE IL MODELLO CHE APPROSSIMA IL PIU' POSSIBILE LO STESSO
    graph_clustering=nx.average_clustering(G)
    graph_avg_path_length=nx.average_shortest_path_length(G)
    random_graph= nx.erdos_renyi_graph(len(G),len(G)/len(G.edges))
    random_graph_clustering=nx.average_clustering(random_graph)
    random_graph_avg_path_length=nx.average_shortest_path_length(random_graph)
    print(f'Coefficiente di clustering del grafo reale {graph_clustering} e average path length {graph_avg_path_length}')
    print(f'Coefficiente di clustering del grafo sintetico {random_graph_clustering} e average path length {random_graph_avg_path_length}')
    partial_degree=0
    for node in G.nodes:
        partial_degree+=G.degree[node]
    avg_degree= partial_degree//len(G)
    small_world_graph = nx.watts_strogatz_graph(len(G), avg_degree, len(G)/len(G.edges))
    small_world_graph_clustering = nx.average_clustering(small_world_graph)
    small_world_graph_avg_path_length = nx.average_shortest_path_length(small_world_graph)
    print(
        f'Coefficiente di clustering del grafo reale {graph_clustering} e average path length {graph_avg_path_length}')
    print(
        f'Coefficiente di clustering del grafo sintetico {small_world_graph_clustering} e average path length {small_world_graph_avg_path_length}')
    #print(len(G))
    #print(len(G.edges))
    #print(len(G)/len(G.edges))
    #print(len(random_graph.edges))
    #print(len(small_world_graph.edges))
    preferential_attachment_graph=nx.barabasi_albert_graph(len(G),avg_degree)
    preferential_attachment_graph_clustering = nx.average_clustering(preferential_attachment_graph)
    preferential_attachment_graph_avg_path_length = nx.average_shortest_path_length(preferential_attachment_graph)
    print(
        f'Coefficiente di clustering del grafo reale {graph_clustering} e average path length {graph_avg_path_length}')
    print(
        f'Coefficiente di clustering del grafo sintetico {preferential_attachment_graph_clustering} e average path length {preferential_attachment_graph_avg_path_length}')

def general_analysis(G):
    print(f"Numero di nodi {len(G.nodes)}")
    print(f"Numero di archi {len(G.edges)}")
    print(f"Raggio {nx.radius(G)}")
    print(f"Diametro {nx.diameter(G)}")
    print(f"Connettività nodi {nx.connectivity.node_connectivity(G)}")
    print(f"Connettività archi {nx.connectivity.edge_connectivity(G)}")
    print(f"Densità {nx.density(G)}")
    partial_degree = 0
    for node in G.nodes:
        partial_degree += G.degree[node]
    avg_degree = partial_degree / len(G)
    print(f"Grado medio {avg_degree}")
    print(f"Average path length del grafo {nx.average_shortest_path_length(G)}")
    print(f"Componenti connesse {nx.number_connected_components(G)}")
    print(f"Coefficiente di clustering medio {nx.average_clustering(G)}")
    print(f"Transitività {nx.transitivity(G)}")


graph=artists_network.create_network()
#degree_centrality(graph['graph'])
#betweenness_centrality(graph['graph'])
#closeness_centrality(graph['graph'])
#eigenvector_analysis(graph['graph'])
#bridge(graph['graph'])
print(graph)
modelling(graph['graph'])
general_analysis(graph['graph'])
nx.write_graphml(graph['graph'],"C:\\Users\\Francesco\\Desktop\\analisi_spotify.graphml")