import sys

def hits(graph, n_iter=5, epison=1e-5):
    auth = dict.fromkeys(graph.nodes, 1.0)
    hubs = dict.fromkeys(graph.nodes, 1.0)

    for _ in range(n_iter):
        last_auth = auth.copy()
        last_hubs = hubs.copy()

        for node in graph.nodes:
            auth[node] = sum_hubs(graph, node, last_hubs)
            hubs[node] = sum_auth(graph, node, last_auth)

        auth = normalize(auth)
        hubs = normalize(hubs)

        delta_auth = [abs(last_auth[k] - auth[k]) for k in auth]
        delta_hubs = [abs(last_hubs[k] - hubs[k]) for k in hubs]
        if sum(delta_auth) + sum(delta_hubs) < epison:
            break

    for key, value in auth.items():
        auth[key] = float(format(value, '.4f'))

    for key, value in hubs.items():
        hubs[key] = float(format(value, '.4f'))

    return (auth, hubs)

def sum_hubs(graph, node, hubs):
    s = 0
    for source in graph.targets[node]:
        s += hubs[source]

    return s

def sum_auth(graph, node, auth):
    s = 0
    for target in graph.sources[node]:
        s += auth[target]

    return s

def normalize(dic):
    norm = sum(dic[k] for k in dic)
    return {k: v / norm for (k, v) in dic.items()}