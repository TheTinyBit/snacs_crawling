from save import *

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def calculate_statistics(G, save=False, output=True, plot=False, log=True, savePlot=False, filename=None):
    # Calculate links and nodes
    max_node = int(max(G.nodes()))
    amt_links = G.number_of_edges()
    amt_nodes = G.number_of_nodes()

    # Calculate some metrics
    density = nx.density(G)
#     avg_clustering = nx.average_clustering(G)

    # Calculate indegree and outdegree
    dg = G.degree()
    idg = G.in_degree()
    odg = G.out_degree()

    # Put indegree and outdegree in a list with value -1
    d_lst = np.zeros(max_node+1) - 1
    i_lst = np.zeros(max_node+1) - 1
    o_lst = np.zeros(max_node+1) - 1

    # Put degrees in numpy array and count empty nodes
    empty = 0
    for node in G:
        node = int(node)
        if dg[node] == 0: empty += 1
        d_lst[node] = dg[node]
        i_lst[node] = idg[node]
        o_lst[node] = odg[node]

    # Remove values -1 (node does not exist)
    d_lst = np.delete(d_lst, np.where(d_lst == -1), axis=0).astype(int)
    i_lst = np.delete(i_lst, np.where(i_lst == -1), axis=0).astype(int)
    o_lst = np.delete(o_lst, np.where(o_lst == -1), axis=0).astype(int)

    # Count unique values and counts
    d_unique, d_counts = np.unique(d_lst, return_counts=True)
    i_unique, i_counts = np.unique(i_lst, return_counts=True)
    o_unique, o_counts = np.unique(o_lst, return_counts=True)

    # Calculate mean values
    mean_dg = np.mean(d_lst)
    mean_idg = np.mean(i_lst)
    mean_odg = np.mean(o_lst)

#     print(len(d_lst))

    # Calculate mean values
    median_dg = np.median(d_lst)
    median_idg = np.median(i_lst)
    median_odg = np.median(o_lst)

    # Save degrees
    # if save:
    #     save_distribution(d_unique, d_counts, filename + '_dg_dist')
    #     save_distribution(i_unique, i_counts, filename + '_idg_dist')
    #     save_distribution(o_unique, o_counts, filename + '_odg_dist')

    statistics = {'amt_links': amt_links, 'amt_nodes': amt_nodes, 'density': density,
                  'mean_dg': mean_dg, 'mean_idg': mean_idg, 'mean_odg': mean_odg,
                  'median_dg': median_dg, 'median_idg': median_idg, 'median_odg': median_odg,
                  'unconnected': d_counts[0],
                  'd_unique': d_unique, 'd_counts': d_counts, 'i_unique': i_unique,
                  'i_counts': i_counts, 'o_unique': o_unique, 'o_counts': o_counts}

    # Save dictionary
    if save:
        keys = ['amt_nodes', 'amt_links', 'density', 'mean_dg', 'mean_idg', 'mean_odg',
                'median_dg', 'median_idg', 'median_odg', 'unconnected']
        save_statistics = {key: statistics[key] for key in keys}

        filename = filename + '_dict'
        filename = check_file(filename)
        write_dict(save_statistics, filename)

    if output:
        print_statistics(statistics, plot, log, savePlot)

    return statistics

def print_statistics(statistics, plot=False, log=True, save=False):
    # Print answers
    print("Number of nodes:\t", statistics['amt_nodes'])
    print("Number of edges:\t", statistics['amt_links'])
    print("Density:\t\t", statistics['density'])
    print()
    print("Mean degree:\t\t", statistics['mean_dg'])
    print("Mean indegree:\t\t", statistics['mean_idg'])
    print("Mean outdegree:\t\t", statistics['mean_odg'])
    print()
    print("Median degree:\t\t", statistics['median_dg'])
    print("Median indegree:\t", statistics['median_idg'])
    print("Median outdegree:\t", statistics['median_odg'])
    print()
    print("Unconnected nodes:\t", statistics['unconnected'])
    #     print("Clustering Coefficient:\t", statistics['avg_clustering'])

    # Plot degrees
    # if plot:
    #     plot_distribution(statistics['d_unique'], statistics['d_counts'], dataset, 'dg_dist', log, save=save)
    #     plot_distribution(statistics['i_unique'], statistics['i_counts'], dataset, 'idg_dist', log, save=save)
    #     plot_distribution(statistics['o_unique'], statistics['o_counts'], dataset, 'odg_dist', log, save=save)

#     # Print Degree
#     print("Degree:")
#     for i in range(len(statistics['d_unique'])): print(int(statistics['d_unique'][i]), "-", statistics['d_counts'][i], end="; ")
#     print("\nIndegree:")
#     for i in range(len(statistics['i_unique'])): print(int(statistics['i_unique'][i]), "-", statistics['i_counts'][i], end="; ")
#     print("\nOutdegree:")
#     for i in range(len(statistics['o_unique'])): print(int(statistics['o_unique'][i]), "-", statistics['o_counts'][i], end="; ")

def clustering_coefficient(G):
    print("Calculating clustering coefficient...")
    total = 0
    for n in G:
        neighbors = G[n]
        amt_neighbors = len(neighbors)
        if amt_neighbors >= 2:
            links = 0
            for w in neighbors:
                for u in neighbors:
                    if u in G[w]: links += 0.5
            total += 2*links/(amt_neighbors*(amt_neighbors-1))
    return total / G.number_of_nodes()

# def plot_distribution(unique, counts, dataset='', filename='', log=False, save=False):
#     plt.figure(figsize=(16,8))
#     plt.bar(unique, counts)
#     if log:
#         plt.xscale('log')
#         plt.yscale('log')
#     plt.xlabel('Degree')
#     plt.ylabel('Counts')
#     plt.title(db + ' - ' + filename)
#     if save:
#         folder = 'results/'
#         filename = check_file(folder + db + '_' + filename, '.png')
#         print("Saving figure to", filename)
#         plt.savefig(filename)
#     plt.show()


def get_largest_wcc(G):
    print("Getting largest WCC...")
    largest_weakly = max(nx.weakly_connected_component_subgraphs(G), key=len)
    return largest_weakly

def get_largest_scc(G):
    print("Getting largest SCC...")
    largest_strong = max(nx.strongly_connected_component_subgraphs(G), key=len)
    return largest_strong

def calculate_fraction(G, Gs):
    node_fraction = 100 * Gs.number_of_nodes() / G.number_of_nodes()
    edge_fraction = 100 * Gs.number_of_edges() / G.number_of_edges()
    print("Node fraction:\t\t", node_fraction)
    print("Edge fraction:\t\t", edge_fraction)
    print()
    return node_fraction, edge_fraction
