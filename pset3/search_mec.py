import numpy as np
import networkx as nx

from matplotlib import pyplot as plt


def covered_edge_neighbors(G):
    cvrd_edgs = []
    edgs = list(G.edges)
    for i, j in edgs:
        print("i,j: ", i, j)
        an_i = nx.ancestors(G, i)
        an_i.add(i)
        an_j = nx.ancestors(G, j)
        if an_j == an_i:
            print(an_i, an_j)
            cvrd_edgs.append((i, j))
    print("cvrd_edgs: ", cvrd_edgs)
    return cvrd_edgs


def search_mec(starting_dag, ending_dag):
    # TODO
    pass


if __name__ == "__main__":
    num_examples = 3

    examples = []
    for ix in range(num_examples):
        a1 = np.loadtxt(f"pset3/mec_examples/starting_dag{ix}.csv")
        a2 = np.loadtxt(f"pset3/mec_examples/ending_dag{ix}.csv")
        starting_dag = nx.from_numpy_array(a1, create_using=nx.DiGraph)
        ending_dag = nx.from_numpy_array(a2, create_using=nx.DiGraph)
        examples.append((starting_dag, ending_dag))

    # PART A
    for starting_dag, _ in examples:
        print(starting_dag)
        num_neighbors = len(covered_edge_neighbors(starting_dag))
        print(num_neighbors)

    # PART B
    for starting_dag, ending_dag in examples:
        pass
        # path = search_mec(starting_dag, ending_dag)
        # print(f"Length of path: {len(path)}")