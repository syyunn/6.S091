import pandas as pd
import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt

from utils import compute_partial_correlation, relabel_nodes

# read imap_samples.csv with numpy
samples = np.genfromtxt('pset3/imap_samples.csv', delimiter=' ')


def minimal_map(samples, perm, alpha):
    G = nx.DiGraph()
    G.add_nodes_from(perm)

    # get all permutations of 2 nodes in perm

    comb = list(itertools.combinations(perm, 2))
    for n1, n2 in comb:
        if perm.index(n1) < perm.index(n2):
            i = n1
            j = n2
        else:
            i = n2
            j = n1

        pre_j = [e for e in perm if perm.index(e) < perm.index(j)]
        pre_j.remove(i)
        S = pre_j

        if compute_partial_correlation(samples, i, j, S) < alpha: # reject the null
            G.add_edge(i, j)

    return G

perm_a = [0, 1, 2, 3, 4]
G_a = minimal_map(samples, perm_a, 0.05)
G_a = relabel_nodes(G_a, perm_a) # add 1 to nodes
nx.draw(G_a, with_labels=True)
plt.show()


if __name__ == "__main__":
    pass
