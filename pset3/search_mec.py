import numpy as np
import networkx as nx

from matplotlib import pyplot as plt


def covered_edge_neighbors(G):
    cvrd_edgs = []
    for i, j in G.edges:
        pa_i = [e for e in G.predecessors(i)]
        pa_i.append(i)
        pa_j = [e for e in G.predecessors(j)]
        if set(pa_i) == set(pa_j):
            cvrd_edgs.append((i, j))
    return cvrd_edgs


def search_mec(starting_dag, ending_dag):
    rev = []
    ending_dag_edges = [e for e in ending_dag.edges]
    for e in starting_dag.edges:
        if e not in ending_dag_edges:
            rev.append(e)
    return rev


if __name__ == "__main__":
    num_examples = 3

    examples = []
    for ix in range(num_examples):
        a1 = np.loadtxt(f"pset3/mec_examples/starting_dag{ix}.csv")
        a2 = np.loadtxt(f"pset3/mec_examples/ending_dag{ix}.csv")
        starting_dag = nx.from_numpy_array(a1, create_using=nx.DiGraph)
        ending_dag = nx.from_numpy_array(a2, create_using=nx.DiGraph)
        assert set([frozenset(e) for e in starting_dag.edges]) == set([frozenset(e) for e in ending_dag.edges])
        examples.append((starting_dag, ending_dag))

    # PART A
    for starting_dag, _ in examples:
        print(starting_dag)
        num_neighbors = len(covered_edge_neighbors(starting_dag))
        print(num_neighbors)

    # PART B
    for starting_dag, ending_dag in examples:
        path = search_mec(starting_dag, ending_dag)
        print(f"Length of path: {len(path)}")