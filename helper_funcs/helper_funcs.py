from collections import defaultdict
import networkx as nx
import plotly.express as px
import pandas as pd
import random


def filter_countries(input_dataframe,
                     filter_column,
                     year=None):
    input_dataframe = input_dataframe[input_dataframe['year'].isin(year)]
    return sorted(list(set(list(input_dataframe[filter_column]))))


def custom_join(strings):
    if len(strings) <= 1:
        return strings[0]
    else:
        return ', '.join(strings[:-1]) + ' & ' + strings[-1]


def generate_network_data(node_list):
    node_counts = {}
    edge_counts = defaultdict(int)
    # Iterate over each sublist
    for sublist in node_list:
        sublist = sorted(sublist)
        sublist = [s.lower() for s in sublist]
        for string in sublist:
            # Update the count for the string
            node_counts[string] = node_counts.get(string, 0) + 1
        for i in range(len(sublist)):
            for j in range(i + 1, len(sublist)):
                # Increment the count for the pair of strings
                edge_counts[(sublist[i], sublist[j])] += 1
    # Convert the dictionary to a list of tuples
    node_weight_list = [(string, count) for string, count in node_counts.items()]
    edge_weight_list = [(pair[0], pair[1], count) for pair, count in edge_counts.items()]
    print(len(node_weight_list))
    return node_weight_list, edge_weight_list


def generate_network(node_list, edge_list):
    # Create an empty graph
    G = nx.Graph()
    # Add nodes to the graph with node size as a node attribute
    color_scale = list(set(px.colors.sequential.Plasma
                           + px.colors.sequential.Viridis
                           + px.colors.sequential.Magma
                           + px.colors.sequential.Turbo
                           + px.colors.sequential.Jet
                           + px.colors.sequential.Plotly3))
    random.seed(47)
    random.shuffle(color_scale)
    print(len(color_scale))
    for index, node in enumerate(node_list):
        G.add_node(node[0], size=node[1], label=f'{node[0]} : {node[1]}', color=color_scale[index])
    # Add edges to the graph with weight as an edge attribute
    for start_node, end_node, weight in edge_list:
        G.add_edge(start_node, end_node, weight=weight)
    return G


def centrality_detection(network_graph, rows=10, algorithms=None):
    column_list = ['Rank']
    ranking_list = [str(i) for i in range(1, rows+1)]
    data_list = [ranking_list]
    if not algorithms or 'eigenvector' in algorithms:
        centrality = nx.eigenvector_centrality(network_graph)
        centrality_list = sorted([v for v, c in centrality.items()], key=lambda x: x[1], reverse=True)[:rows]
        column_list.append('Centrality Ranking')
        data_list.append(centrality_list)
    if not algorithms or 'page_rank' in algorithms:
        page_rank = nx.pagerank(network_graph)
        page_rank_list = sorted([v for v, c in page_rank.items()], key=lambda x: x[1], reverse=True)[:rows]
        column_list.append('PageRank Ranking')
        data_list.append(page_rank_list)
    if not algorithms or 'betweenness' in algorithms:
        betweenness = nx.betweenness_centrality(network_graph)
        betweenness_list = sorted([v for v, c in betweenness.items()], key=lambda x: x[1], reverse=True)[:rows]
        column_list.append('Betweenness Ranking')
        data_list.append(betweenness_list)
    if not algorithms or 'closeness' in algorithms:
        closeness_centrality = nx.closeness_centrality(network_graph)
        closeness_list = sorted([v for v, c in closeness_centrality.items()], key=lambda x: x[1], reverse=True)[:rows]
        column_list.append('Closeness Ranking')
        data_list.append(closeness_list)
    if not algorithms or 'degree' in algorithms:
        degree = nx.degree_centrality(network_graph)
        degree_list = sorted([v for v, c in degree.items()], key=lambda x: x[1], reverse=True)[:rows]
        column_list.append('Degree Ranking')
        data_list.append(degree_list)
    if not algorithms or 'second_order' in algorithms:
        second_order = nx.second_order_centrality(network_graph)
        second_order_list = sorted([v for v, c in second_order.items()], key=lambda x: x[1], reverse=True)[:rows]
        column_list.append('SecondOrder Ranking')
        data_list.append(second_order_list)
    algo_dataframe = pd.DataFrame(zip(*data_list),
                                  columns=column_list)
    return algo_dataframe


def community_detection(network_graph):
    communities = nx.community.greedy_modularity_communities(network_graph, weight='weight', cutoff=3)[:5]
    for index, community in enumerate(communities):
        communities[index] = custom_join(list(community))
    return communities


def clique_detection(network_graph):
    cliques = list(nx.find_cliques(network_graph))[:5]
    cliques.sort(key=len, reverse=True)
    for index, clique in enumerate(cliques):
        cliques[index] = custom_join(list(clique))
    return cliques
