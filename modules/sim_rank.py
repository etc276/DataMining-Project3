import numpy as np

def sim_rank(graph, C=0.9, n_iter=10):
    num_node = len(graph.nodes)
    S = np.identity(num_node)

    for _ in range(n_iter):
        last_S = S.copy()

        for i in range(num_node):
            for j in range(num_node):
                a, b = str(i), str(j)
                len_a = len(graph.targets[a])
                len_b = len(graph.targets[b])
                if a == b or len_a == 0 or len_b == 0:
                    continue

                tmp = 0
                for sa in graph.targets[a]:
                    for sb in graph.targets[b]:
                        tmp += last_S[int(sa) - 1][int(sb) - 1]

                S[i][j] = C / (len_a * len_b) * tmp
    
    return S


        