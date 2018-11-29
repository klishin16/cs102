from api import get_friends
from igraph import Graph, plot
import igraph
import numpy as np
import time
from typing import Union, List, Tuple
import math


def get_network(users_ids: list, as_edgelist=True) -> Union[List[List[int]], List[Tuple[int, int]]]:
    matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]
    edgelist = []
    for id in range(len(users_ids)):
        time.sleep(0.4)
        response = get_friends(users_ids[id], 'bdate')
        if response.get('error'):
            continue
        else:
            friends = [friend["id"] for friend in response['response']['items']]
            for user in range(len(users_ids)):
                for friend in friends:
                    if users_ids[user] == friend:
                        if as_edgelist:
                            edgelist.append((id, user))
                        else:
                            matrix[id][user] = 1
    if as_edgelist:
        return edgelist
    else:
        return matrix


def plot_graph(edgelist: list) -> None:
    vertices = [i for i in range(edgelist[-1][0] + 1)]

    g = Graph(vertex_attrs={"label": vertices}, edges=edgelist, directed=False)

    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    g.simplify(multiple=True, loops=True)
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)
