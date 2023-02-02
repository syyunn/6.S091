import pandas as pd
import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt

from utils import compute_pvalue, relabel_nodes

samples = np.genfromtxt('pset3/imap_samples.csv', delimiter=' ')


def minimal_map(samples, perm, alpha):
    G = nx.DiGraph()
    G.add_nodes_from(perm)

    comb = list(itertools.combinations(perm, 2))
    for n1, n2 in comb:
        if perm.index(n1) < perm.index(n2):
            i = n1
            j = n2
        else:
            i = n2
            j = n1
        print("i,j:", i, j)
        pre_j = [e for e in perm if perm.index(e) < perm.index(j)]
        pre_j.remove(i)
        print("pre_j:", pre_j)

        S = pre_j

        if compute_pvalue(samples, i, j, S) < alpha: 
            # reject the null, i.e. add edge i->j
            G.add_edge(i, j)

    return G

perm_a = [0, 1, 2, 3, 4]
G_a = minimal_map(samples, perm_a, 0.05)
G_a = relabel_nodes(G_a, perm_a) # add 1 to nodes

print("G_a.edges:", len(G_a.edges))
nx.draw(G_a, with_labels=True)
plt.savefig('pset3/tex/images/pb1a.png')
plt.close()

perm_b = [4, 3, 0, 1, 2]
G_b = minimal_map(samples, perm_b, 0.05)
G_b = relabel_nodes(G_b, perm_b) # add 1 to nodes
nx.draw(G_b, with_labels=True)
plt.savefig('pset3/tex/images/pb1b.png')
plt.close()

perm_c = [4, 3, 2, 1, 0]
G_c = minimal_map(samples, perm_c, 0.05)
G_c = relabel_nodes(G_c, perm_c) # add 1 to nodes
nx.draw(G_c, with_labels=True)
plt.savefig('pset3/tex/images/pb1c.png')
plt.close()

if __name__ == "__main__":
    pass
