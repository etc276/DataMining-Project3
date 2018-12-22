import sys
import copy
import numpy as np
from collections import defaultdict

from modules.hits import hits
from modules.page_rank import page_rank
from modules.sim_rank import sim_rank

class Graph:

    def __init__(self, nodes, sources, targets):
        self.nodes = nodes
        self.sources = sources
        self.targets = targets

def get_graph(argv):

    if len(argv) < 1:
        print('Error')
        exit(-1)

    fname = argv[1]
    nodes = set()
    sources = defaultdict(list)
    targets = defaultdict(list)

    with open(fname, 'r') as fp:
        for line in fp:
            a, b = line.rstrip('\n').split(',')
            a, b = int(a), int(b)
            nodes.add(a)
            nodes.add(b)
            sources[a].append(b)
            targets[b].append(a)

    return Graph(nodes, sources, targets)

def get_max_index(dic):
    max_index, max_value = -1, -1
    for (key, value) in dic.items():
        if key != 1 and value > max_value:
            max_index = key
            max_value = value

    return max_index

if __name__=='__main__':

    # Read data and return graph
    graph = get_graph(sys.argv)

    # HITS and PageRank
    ## Before
    auth, hubs = hits(graph)
    ranks = page_rank(graph, d=0.3)
    print('\nOriginal graph')
    print('auth:', auth)
    print('hubs:', hubs)
    print('rank:', ranks)

    ## After
    graph_copy = copy.deepcopy(graph)
    max_index_auth = get_max_index(auth)
    max_index_hubs = get_max_index(hubs)
    graph_copy.sources[1].append(max_index_auth)
    graph_copy.targets[1].append(max_index_hubs)
    auth, hubs = hits(graph_copy)
    ranks = page_rank(graph_copy, d=0.15)
    print('\nAfter add one link ...')
    print('auth:', auth)
    print('hubs:', hubs)
    print('rank:', ranks)

    # # Sim Rank
    # S = sim_rank(graph)
    # print('\nSimRank:')
    # print(S)