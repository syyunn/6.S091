import pandas as pd
import numpy as np

from more_itertools import powerset
from itertools import combinations

import networkx as nx
import matplotlib.pyplot as plt

X = pd.read_csv('pset2/code/problem2/pcalg_samples.csv',delimiter=' ', header=None, index_col=False)
X.columns = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7']

from sklearn.linear_model import LinearRegression

def regress_linear(X, y):
    reg = LinearRegression().fit(X, y)
    return reg.coef_

def compute_partial_correlation(samples, i, j, S):
    Xi = samples[[f'X{i}']]
    Xj = samples[[f'X{j}']]

    if len(S) == 0:
        corr = np.corrcoef(np.squeeze(Xi), np.squeeze(Xj))[0, 1]        
        return corr

    S = samples[[f'X{s}' for s in S]]

    bi = regress_linear(S, Xi)
    bj = regress_linear(S, Xj)

    Ri = Xi - np.dot(S, bi.T)
    Rj = Xj - np.dot(S, bj.T)

    corr = np.corrcoef(np.squeeze(Ri), np.squeeze(Rj))[0, 1]

    return corr

r1 = compute_partial_correlation(X, 1, 7, [3, 4])
r2 = compute_partial_correlation(X, 1, 7, [])

ra = compute_partial_correlation(X, 1, 4, [])
rb = compute_partial_correlation(X, 1, 4, [2, 3])

def fisherz(r):
    return 0.5 * np.log((1 + r) / (1 - r))

def ztransf(samples, i, j, S):
    r = compute_partial_correlation(samples, i, j, S)
    return np.sqrt(samples.shape[0]- len(S)-3) * fisherz(r)

z1 = ztransf(X, 1, 7, [3, 4])
z2 = ztransf(X, 1, 7, [])

xzc = ztransf(X, 1, 4, [2, 3])

def pval(samples, i, j, S):
    from scipy.stats import norm
    z = ztransf(samples, i, j, S)
    return 2 * (1 - norm.cdf(np.abs(z)))

pval1 = pval(X, 1, 7, [3, 4])
pval2 = pval(X, 1, 7, [])

pvald = pval(X, 1, 4, [2, 3])

def pcalg_skeleton(samples, alpha):
    import networkx as nx
    # create complete graph
    G = nx.complete_graph(len(samples.columns))
    
    # relabel nodes not to start from 0 but from 1    
    mapping = {}
    for i in range(0, len(samples.columns)):
        mapping[i] = i+1
    G = nx.relabel_nodes(G, mapping)

    # define sepeartaor
    sep = dict() 

    # initialize d
    d = 0

    def exists(G, d):
        for i, j in G.edges:
            neighbors = [n for n in G.neighbors(i)]
            neighbors.remove(j)
            if len(neighbors) >= d:
                return True
        return False

    while exists(G, d):
        print("d:", d)
        for i, j in G.edges:
            neighbor_i = [n for n in G.neighbors(i)]
            neighbor_i.remove(j)
            SS = list(powerset(neighbor_i))
            for S in SS:
                if len(S) == d:
                    pval_ij_S = pval(samples, i, j, S)
                    if pval_ij_S > alpha:
                        if G.has_edge(i, j):
                            print("remove")
                            print(i, j, S, pval_ij_S)
                            G.remove_edge(i, j)
                            sep[(i, j)] = S

            neighbor_j = [n for n in G.neighbors(j)]
            if i in neighbor_j:
                neighbor_j.remove(i)

            SS = list(powerset(neighbor_j))
            for S in SS:
                if len(S) == d:
                    pval_ji_S = pval(samples, j, i, S)
                    if pval_ji_S > alpha:
                        if G.has_edge(i, j):
                            print("remove")
                            print(i, j, S, pval_ji_S)
                            G.remove_edge(i, j)
                            sep[(i, j)] = S
        d = d + 1            

    print("alpha:", alpha)
    print("#edge", G.number_of_edges())
    import matplotlib.pyplot as plt
    nx.draw(G, with_labels=True)
    plt.savefig(f"./pset2/code/problem2/skel_{alpha}.png")
    plt.close()
    return G, sep

# pcalg_skeleton(X, 0.05)
# pcalg_skeleton(X[:500], 0.2)
# pcalg_skeleton(X[:500], 0.001)

G, s = pcalg_skeleton(X, 0.05)

unshielded = []
for k in G.nodes:
    neighbors = [n for n in G.neighbors(k)]
    if len(neighbors) < 2:
        continue
    else:
        print(k)
        colliders = list(combinations(neighbors, 2))
        # print(colliders)
        for i, j in colliders:
            if not G.has_edge(i, j):
                if k not in s[(i, j)]:
                    print("add unshilded")
                    unshielded.append((i, k, j))
print(unshielded)


# Meek's rule
# First change the graph to the directed one
G = G.to_directed()

# Remove unshielded colliders
G.remove_edges_from([(3,1), (3,2)])

# Rule1 
print("Rule1")
# we have two directed edges (1,3), (2,3)
d_edges = [(1,3), (2,3)]
for k, i in d_edges:
    print("handling edge", k, "->", i)
    k_neighbors = [n for n in G.neighbors(k)] + [k]
    not_adjacent_to_k = [n for n in G.nodes if n not in k_neighbors]
    for j in not_adjacent_to_k:
        if G.has_edge(j, i):
            print("new orient")
            print(i, j)
            G.remove_edge(j, i)

nx.draw(G, with_labels=True)
plt.show()

# Rule2
print("Rule2")
# find any directed edges 
for i, j in G.edges:
    if not G.has_edge(j, i): # if i -> j
       for k in G.neighbors(j):
           if G.has_edge(j, k):
               if not G.has_edge(k, j): # if j -> k
                   if G.has_edge(k, i) and G.has_edge(i, k): # then we assign i -> k
                       print("new orient")
                       print(i, k)
                       G.remove_edge(k, i) 

# Rule3
print("Rule3")
for i, u in G.edges:
    if G.has_edge(u, i): # i-u
        for v in G.neighbors(i):
            if G.has_edge(v, i) and G.has_edge(i, v): # i-v
                for j in G.neighbors(u):
                    if G.has_edge(u, j) and not G.has_edge(j, u) and G.has_edge(v, j) and not G.has_edge(j, v):
                        if G.has_edge(i, j) and G.has_edge(j, i):
                            print("new orient")
                            print(i, j)
                            G.remove_edge(j, i) 

# Rule4
print("Rule4")
for i, u in G.edges:
    if G.has_edge(u, i): # i-u
        for v in G.neighbors(i):
            if G.has_edge(v, i) and G.has_edge(i, v): # i-v
                if G.has_edge(u, v) and not G.has_edge(v, u):
                    for j in G.neighbors(v):
                        if G.has_edge(v, j) and not G.has_edge(j, v):
                            if G.has_edge(i, j) and not G.has_edge(j, i):
                                print("new orient")
                                print(i, j)
                                G.remove_edge(j, i)

if __name__ == '__main__':
    pass

