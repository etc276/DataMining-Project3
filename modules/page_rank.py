
def page_rank(graph, n_iter=10, d=0.15):
    num_nodes = len(graph.nodes)
    ranks = dict.fromkeys(graph.nodes, 1.0 / num_nodes)

    for _ in range(n_iter):     # repeat n times
        last_ranks = ranks.copy()
        for node in graph.nodes:    # iter all nodes
            rank = 0
            for source in graph.targets[node]:
                tmp = last_ranks[source] / len(graph.sources[source])
                # print(node, source, tmp)
                rank += tmp
            ranks[node] = d / num_nodes + (1 - d) * rank

    for key, value in ranks.items():
        ranks[key] = float(format(value, '.4f'))
        
    return ranks