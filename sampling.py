from save import *
from stats import *

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import random

def generate_seed_list(G, length=100, seed=0):
    np.random.seed(seed) # Set seed
    seed_list = np.random.choice(G.nodes(), length, replace=False) # Randomly select 100 nodes
    for key, seed in enumerate(seed_list):
        if not G.neighbors(seed):
            cont = True
            while cont:
                seed = np.random.choice(G.nodes(), 1)[0]
                if G.neighbors(seed):
                    cont = False
            seed_list[key] = seed
    check_seed_list(G, seed_list)
    return seed_list

def check_seed_list(G, seed_list):
    for seed in seed_list:
        if not G.neighbors(seed):
            print("Found empty one...")
    return

def print_iteration(iteration, crawled, found):
    print("Iteration:", iteration, end="\t- ", flush=True)
    print("Found:", found, end="\t- ", flush=True)
    print("Crawled:", crawled, flush=True)

def print_reduction(G, Gs, crawled, iterations, num_walkers):
    print()
    eff = crawled / (iterations * num_walkers)
    print("Efficiency:\t", 100 * eff, '%')
    node_subsize = Gs.number_of_nodes() / G.number_of_nodes()
    print("Node Subsize:\t", 100 * round(node_subsize,4), '%')
    edge_subsize = Gs.number_of_edges() / G.number_of_edges()
    print("Edge Subsize:\t", 100 * round(edge_subsize,4), '%')

def bfs(G, seed_list, max_iterations=1000000, sample_size=0.01, sample_type='nodes', seed=0):
    np.random.seed(seed)
    random.seed(seed)

    if sample_type == 'nodes':
        size = G.number_of_nodes()
        desired_size = size * sample_size
        # print("Desired size:\t", int(desired_size))

    crawled_nodes = np.array(seed_list)  # Nodes in subgraph, initialize on seed_list
    next_nodes = np.array(seed_list) # List of nodes explored next, initialize on seed_list
    found_nodes = np.array(seed_list) # Nodes in subgraph, initialize on seed_list

    # print_iteration(0, 0, len(seed_list))
    walk_lengths = {0: [0, len(seed_list)]}

    i = 0
    cur_size = 0
    complete = 1
    prev_len = len(found_nodes)
    while cur_size < desired_size and i <= max_iterations:

        node = next_nodes[0]                                # Pick first node from stack
        crawled_nodes = np.append(crawled_nodes, node)      # Append node to traversed nodes
        next_nodes = np.delete(next_nodes, 0)               # Delete node from stack
        neighbors = G.neighbors(node)                       # Get neighbor list

        next_nodes = np.append(next_nodes, neighbors)       # Append neighbors to stack
        _, idx = np.unique(next_nodes, return_index=True)   # Get indexes of unique vales
        next_nodes = next_nodes[np.sort(idx)]               # Set unique values in order

        found_nodes = np.append(found_nodes, neighbors)     # Append neighbors to found nodes
        found_nodes = np.unique(found_nodes)                # Remove duplicate entries in found

        if sample_type == 'nodes':
            cur_size = len(found_nodes)
            crawl_size = len(crawled_nodes)
        elif sample_type == 'edges': cur_size = len(G.subgraph(crawled_nodes).number_of_edges())

        if i % 100 == 0 and cur_size > prev_len:
            walk_lengths[i] = [crawl_size, cur_size]
            prev_len = cur_size

        i += 1

        if i % 1000 == 0:
            pass
            # print_iteration(i, crawl_size, cur_size)

    if i > max_iterations:
        complete = 0
        # print("\n!!!-ENDED PREMATURELY-!!!")

    # print_iteration(i, crawl_size, cur_size)
    Gs = G.subgraph(found_nodes.astype(int)) # New subgraph
    # print_reduction(G, Gs, crawl_size, i, 1)
    return Gs, walk_lengths, i, complete

def rw(G, seed_list, max_iterations=100000, sample_size=0.01, sample_type='nodes', seed=0, using='none', p=0.15):
    np.random.seed(seed)
    random.seed(seed)

    num_walkers = len(seed_list) # Amount of walkers

    if sample_type == 'nodes':
        size = G.number_of_nodes()
        desired_size = size * sample_size
        # print("Desired size:\t", int(desired_size))

    crawled_nodes = np.array(seed_list)  # Nodes in subgraph, initialize on seed_list
    next_nodes = np.array(seed_list) # List of nodes explored next, initialize on seed_list
    found_nodes = np.array(seed_list) # Nodes in subgraph, initialize on seed_list

    # print_iteration(0, 0, num_walkers)
    walk_lengths = {0: [0, num_walkers]}

    i = 0
    cur_size = 0
    complete = 1
    prev_len = len(found_nodes)
    while cur_size < desired_size and i <= max_iterations:

        for w in range(num_walkers):

            if random.uniform(0, 1) > p:
                neighbors = G.neighbors(next_nodes[w]) # Get neighbor list
                found_nodes = np.append(found_nodes, neighbors)
                if neighbors:
                    next_nodes[w] = np.random.choice(neighbors, 1)
            else:
                if using == 'restart':
                    next_nodes[w] = seed_list[w]
                elif using == 'jump':
                    next_nodes[w] = np.random.choice(found_nodes)
                elif using == 'none':
                    print("!!!-This should never happen.-!!!")

        crawled_nodes = np.append(crawled_nodes, next_nodes) # Append new nodes to list
        crawled_nodes = np.unique(crawled_nodes) # Remove duplicate entries
        found_nodes = np.unique(found_nodes) # Remove duplicate entries

        if sample_type == 'nodes':
            cur_size = len(found_nodes)
            crawl_size = len(crawled_nodes)
        elif sample_type == 'edges': cur_size = len(G.subgraph(crawled_nodes).number_of_edges())

        if i % 10 == 0 and cur_size > prev_len:
            walk_lengths[i] = [crawl_size,cur_size]
            prev_len = cur_size

        i += 1

        if i % 1000 == 0:
            pass
            # print_iteration(i, crawl_size, cur_size)



    if i > max_iterations:
        # print("\n!!!-ENDED PREMATURELY-!!!")
        complete = 0

    # print_iteration(i, crawl_size, cur_size)
    Gs = G.subgraph(found_nodes.astype(int)) # New subgraph
    # print_reduction(G, Gs, crawl_size, i, num_walkers)
    return Gs, walk_lengths, i, complete

def mhrw(G, seed_list, max_iterations=100000, sample_size=0.01, sample_type='nodes', seed=0):
    np.random.seed(seed)
    random.seed(seed)

    num_walkers = len(seed_list) # Amount of walkersv

    if sample_type == 'nodes':
        size = G.number_of_nodes()
        desired_size = size * sample_size
        # print("Desired size:\t", int(desired_size))

    crawled_nodes = np.array(seed_list)  # Nodes in subgraph, initialize on seed_list
    next_nodes = np.array(seed_list) # List of nodes explored next, initialize on seed_list
    found_nodes = np.array(seed_list) # Nodes in subgraph, initialize on seed_list

    # print_iteration(0, 0, num_walkers)
    walk_lengths = {0: [0, num_walkers]}

    i = 0
    cur_size = 0
    complete = 1
    prev_len = len(found_nodes)
    while cur_size < desired_size and i <= max_iterations:

        for w in range(num_walkers):
            neighbors = G.neighbors(next_nodes[w])
            if neighbors:
                found_nodes = np.append(found_nodes, neighbors)
                candidate_node = np.random.choice(neighbors)
                p = np.random.random(1)
                candidate_neighbors = G.neighbors(candidate_node)
                if candidate_neighbors:
                    prob = min(1,len(neighbors) / len(candidate_neighbors))
                    if p < prob:
                        next_nodes[w] = candidate_node

        crawled_nodes = np.append(crawled_nodes, next_nodes) # Append new nodes to list
        crawled_nodes = np.unique(crawled_nodes) # Remove duplicate entries
        found_nodes = np.unique(found_nodes) # Remove duplicate entries

        if sample_type == 'nodes':
            cur_size = len(found_nodes)
            crawl_size = len(crawled_nodes)
        elif sample_type == 'edges': cur_size = len(G.subgraph(crawled_nodes).number_of_edges())

        if i % 10 == 0 and cur_size > prev_len:
            walk_lengths[i] = [crawl_size, cur_size]
            prev_len = cur_size

        i += 1

        if i % 10000 == 0:
            pass
            # print_iteration(i, crawl_size, cur_size)


    if i > max_iterations:
        complete = 0
        # print("\n!!!-ENDED PREMATURELY-!!!")

    # print_iteration(i, crawl_size, cur_size)
    Gs = G.subgraph(found_nodes.astype(int)) # New subgraph
    # print_reduction(G, Gs, crawl_size, i, num_walkers)
    return Gs, walk_lengths, i, complete
