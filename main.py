from save import *
from stats import *
from sampling import *

## Imports ##
import sys
import time
import datetime
import os.path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

import random
import pickle

def print_help(possible_parameters):
    datasets = possible_parameters[0]
    algorithms = possible_parameters[1]
    percentages = possible_parameters[2]
    walkers = possible_parameters[3]
    seeds = possible_parameters[4]

    print("POSSIBLE CONFIGURATIONS")
    print("  Datasets:\t{", end='')
    print("all: ALL, ", end='')
    for i in range(len(datasets)):
        print(str(i)+': '+datasets[i], end='')
        if i != len(datasets) - 1: print(', ', end='')
    print("}\n  Algorithms:\t{", end='')
    for i in range(len(algorithms)):
        print(str(i)+': '+algorithms[i], end='')
        if i != len(algorithms) - 1: print(', ', end='')
    print("}\n  Percentages:\t{", end='')
    for i in range(len(percentages)):
        print(str(i)+': '+str(percentages[i]), end='')
        if i != len(percentages) - 1: print(', ', end='')
    print("}\n  Walkers:\t{", end='')
    for i in range(len(walkers)):
        print(str(i)+': '+str(walkers[i]), end='')
        if i != len(walkers) - 1: print(', ', end='')
    print("}\n  Seeds:\t{", end='')
    for i in range(len(seeds)):
        print(str(i)+': '+str(seeds[i]), end='')
        if i != len(seeds) - 1: print(', ', end='')
    print("}")

def st(output=True):
    start = time.time()
    st = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    if output: print(st)
    return start

def et(start, output=True):
    end = time.time()
    dif = end - start
    st = datetime.datetime.fromtimestamp(dif - 3600).strftime('%H:%M:%S')
    if output: print(st)
    return dif

def load_pickle_dataset(dataset, path):
    print("\nLOADING DATASET -", dataset)
    t = st()
    G = nx.read_gpickle(path + dataset + '.pkl')
    et(t)
    print("# Nodes:\t", G.number_of_nodes())
    print("# Edges:\t", G.number_of_edges())
    return G

def main(parameters, possible_parameters, G=None, path='.'):
    # datasets = ['youtube', 'flickr', 'livejournal', 'orkut']
    # algorithms = ['rw', 'rwr', 'rwj', 'mhrw', 'bfs']
    # walkers = [10, 100, 1000]
    # seeds = range(0,3)

    # possible_parameters[0][a[0]]
    #
    # dataset = datasets[a[0]]
    # algorithm = algorithms[a[1]]
    # percentage = a[2]
    # walkers = a[3]
    # seed = a[4]

    # Set parameters
    dataset = parameters[0]
    algorithm = parameters[1]
    percentage = parameters[2]
    walkers = parameters[3]
    seed = parameters[4]

    # Find index of dataset and algorithm
    index_dataset = possible_parameters[0].index(parameters[0])
    index_algorithm = possible_parameters[1].index(parameters[1])
    index_percentage = possible_parameters[2].index(parameters[2])
    index_walkers = possible_parameters[3].index(parameters[3])
    index_seed = possible_parameters[4].index(parameters[4])

    # print("\nUSING PARAMETERS")
    # print("Dataset:\t\t", dataset)
    # print("Algorithm:\t\t", algorithm)
    # print("Percentage:\t\t", percentage)
    # print("Number of seeds:\t", walkers)
    # print("Seed:\t\t\t", seed)

    # Load dataset
    if not G: G = load_pickle_dataset(dataset)

    # Get statistics
    # print("\nCALCULATING STATISTICS")
    # statistics = calculate_statistics(G, save=False, output=True, plot=False, log=True, savePlot=False, filename=dataset) # 8 / 17 / 4 / 9 seconds
    # print_statistics(statistics, plot=True, log=True, save=True, filename='results/stats/'+dataset)

    # t = st()
    # cc = clustering_coefficient(G)
    # et(t)
    # print("Clustering coefficient:\t", cc)

    # Compute weakly and strongly connected component
    # print("\nWEAKLY CONNECTED COMPONENT")
    # t = st()
    # G_wcc = get_largest_wcc(G) # ? / ? / 1m / 40m
    # et(t)
    #
    # print("\nWeakly:")
    # wcc_nf, wcc_ef = calculate_fraction(G, G_wcc)
    # wcc_stats = calculate_statistics(G_wcc, save=True, filename='results/stats/'+dataset+'_wcc')
    # print_statistics(wcc_stats)
    #
    # print("\nSTRONGLY CONNECTED COMPONENT")
    # t = st()
    # G_scc = get_largest_scc(G) # ? / ? / 2m / 45m
    # et(t)
    #
    # print("\nStrongly:")
    # scc_nf, scc_ef = calculate_fraction(G, G_scc)
    # scc_stats = calculate_statistics(G_scc, save=True, filename='results/stats/'+dataset+'_scc')
    # print_statistics(scc_stats)

    # print("\nSAMPLING")
    # filename = dataset + '-' + algorithm + '-' + str(percentage) + '-' + str(walkers) + '-' + str(seed)
    filename2 = str(index_dataset)+'_'+str(index_algorithm)+'_'+str(index_percentage)+'_'+str(index_walkers)+'_'+str(index_seed)

    max_iterations = 1000000 / walkers
    seed_list = generate_seed_list(G, walkers, seed)
    sample_size = 0.01 * percentage
    t = st()
    if algorithm == 'bfs':
        max_iterations *= walkers # Make correction because we have no walkers
        Gs, fl, iterations, complete = bfs(G, seed_list, max_iterations=max_iterations, sample_size=sample_size, sample_type='nodes', seed=seed)
    elif algorithm == 'rw':
        p = -1
        using = 'none'
        Gs, fl, iterations, complete = rw(G, seed_list, max_iterations=max_iterations, sample_size=sample_size, sample_type='nodes', seed=seed, using=using, p=p)
    elif algorithm == 'rwr':
        p = 0.15
        using = 'restart'
        Gs, fl, iterations, complete = rw(G, seed_list, max_iterations=max_iterations, sample_size=sample_size, sample_type='nodes', seed=seed, using=using, p=p)
    elif algorithm == 'rwj':
        p = 0.15
        using = 'jump'
        Gs, fl, iterations, complete = rw(G, seed_list, max_iterations=max_iterations, sample_size=sample_size, sample_type='nodes', seed=seed, using=using, p=p)
    if algorithm == 'mhrw':
        Gs, fl, iterations, complete = mhrw(G, seed_list, max_iterations=max_iterations, sample_size=sample_size, sample_type='nodes', seed=seed)
    crawl_time = et(t)

    filename = path + 'subs/' + filename2
    filename = check_file(filename, '.pkl')
    nx.write_gpickle(Gs, filename, protocol=2)
    # print("Subgraph exported to", filename)

    flfile = check_file('results/iters/iter' + filename2)
    write_dict(fl, flfile)

    statistics = calculate_statistics(Gs, save=True, output=False, plot=False, log=True, savePlot=False, filename='results/stats'+filename2) # 8 / 17 / 4 / 9 seconds
    keys = ['amt_nodes', 'amt_links', 'density', 'mean_dg', 'mean_idg', 'mean_odg',
            'median_dg', 'median_idg', 'median_odg', 'unconnected']

    outputfile = check_file('results/runs/run'+filename2)
    with open(outputfile, 'w') as file:
        file.write(str(a[0])+','+str(a[1])+','+str(a[2])+','+str(a[3])+','+str(a[4]))
        file.write(','+str(crawl_time))
        for key in keys:
            file.write(','+str(statistics[key]))
        file.write(','+str(iterations)+','+str(complete))
        file.write("\n")

if __name__ == "__main__":
    path = '/data/s1314106/SNA/paper/' # Path to data

    # Create directories for results
    if not os.path.isdir("results"): os.mkdir("results") # Store results
    if not os.path.isdir("results/runs"): os.mkdir("results/runs") # Store runs
    if not os.path.isdir("results/iters"): os.mkdir("results/iters") # Store iterations
    if not os.path.isdir("results/stats"): os.mkdir("results/stats") # Store statistics
    if not os.path.isdir(path + "subs"): os.mkdir(path + "subs") # Store subgraphs

    # Available parameters
    datasets = ['youtube', 'flickr', 'livejournal', 'orkut']
    algorithms = ['bfs', 'rw', 'rwr', 'rwj', 'mhrw']
    percentages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50] # , 60, 70, 80
    walkers = [10, 100, 1000, 10000]
    seeds = [0, 1, 2]
    possible_parameters = [datasets, algorithms, percentages, walkers, seeds]

    # Set parameters if available (choosing a specific configuration)
    cont = True # Boolean to run or not
    parameters = []
    number_of_arguments = len(sys.argv)
    if number_of_arguments > 1:
        if sys.argv[1] == 'help':
            print_help(possible_parameters)
            cont = False
        elif sys.argv[1] != 'all': parameters.insert(0, [datasets[int(sys.argv[1])]]);
        else: parameters.insert(0, datasets)
        if number_of_arguments > 2: parameters.insert(1, [algorithms[int(sys.argv[2])]]);
        else: parameters.insert(1, algorithms)
        if number_of_arguments > 3: parameters.insert(2, [percentages[int(sys.argv[3])]]);
        else: parameters.insert(2, percentages)
        if number_of_arguments > 4: parameters.insert(3, [walkers[int(sys.argv[4])]]);
        else: parameters.insert(3, walkers)
        if number_of_arguments > 5: parameters.insert(4, [seeds[int(sys.argv[5])]]);
        else: parameters.insert(4, seeds)
    else:
        parameters = [datasets, algorithms, percentages, walkers, seeds]

    # # Single run
    # if a:
    #     G = load_pickle_dataset(datasets[a[0]], path)
    #     print("Starting at ", end='')
    #     t = st()
    #     main(a, G, path='/data/s1314106/SNA/paper/')
    #     print("Ended. It took ", end='')
    #     et(t)
    # else:

    if cont:
        # Full runs
        print("Using parameters:", parameters)
        print("Starting at ", end='')
        t = st()
        for i in parameters[0]:
            G = load_pickle_dataset(i, path)
            for j in parameters[1]:
                for k in parameters[2]:
                    for l in parameters[3]:
                        for m in parameters[4]:
                            print(parameters)
                            a = [i, j, k, l, m]
                            filename = 'results/runs/run'+str(i)+'_'+str(j)+'_'+str(k)+'_'+str(l)+'_'+str(m)
                            if not os.path.exists(filename + '.csv'):
                                print('\nConfig:', a)
                                main(a, possible_parameters, G, path='/data/s1314106/SNA/paper/')
                            else:
                                print('\nConfig:', a, 'exists already. Going to next config.')
        print("\nEnded. It took ", end='')
        et(t)

    # # # Failed runs
    # print("Starting at ", end='')
    # t = st()
    # # for i in range(len(datasets)):
    # i = 2
    # G = load_pickle_dataset(datasets[i], path)
    # # for j in range(len(algorithms)):
    # j = 4
    # for k in percentages:
    #     for l in walkers:
    #         for m in seeds:
    #             filename = 'runs/run'+str(i)+'_'+str(j)+'_'+str(k)+'_'+str(l)+'_'+str(m)
    #             if not os.path.exists(filename + '.csv'):
    #                 a = [i, j, k, l, m]
    #                 print('\nConfig:', a)
    #                 main(a, G, path='/data/s1314106/SNA/paper/')
    # print("\nEnded. It took ", end='')
    # et(t)
