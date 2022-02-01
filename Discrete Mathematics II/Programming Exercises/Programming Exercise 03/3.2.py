"""
This program computes the RCSPP as stated in
Programming Exercise 3.2

File system should be setup as follows:

├── data/
│   ├── graph1_2.txt
│   ├── graph4_2.txt
│   ├── grid1.txt
│   └── grid2.txt
├── DiGraph.py
└── 3.2.py

Group: Dallmer, Kane, Jankowsky

"""

import os
import time

from pyscipopt import Model, quicksum

from DiGraph import DiGraph


def rcspp(G, s, t, l):
    """
    Defines the model for the Resource Constrained Shortest Path Problem
    with parameters:

    G       :   Graph
    s       :   starting node
    t       :   end node
    l       :   resource limit
    """

    arcs = G.arcs()
    vertices = G.V()
    in_arcs, out_arcs = G.in_out_arcs()
    c = G.costs()
    r = G.resources()

    model = Model("RCSPP")

    """define variables"""
    x = {}
    for a in arcs:
        x[a] = model.addVar(vtype="B")

    """define contraints"""
    # chosen path is st-path:
    model.addCons((quicksum(x[a] for a in out_arcs[s])
                   - quicksum(x[a] for a in in_arcs[s])) == 1)
    model.addCons((quicksum(x[a] for a in out_arcs[t])
                   - quicksum(x[a] for a in in_arcs[t])) == -1)
    for u in vertices:
        if u != s and u != t:
            model.addCons((quicksum(x[a] for a in out_arcs[u])
                           - quicksum(x[a] for a in in_arcs[u])) == 0)
    # resource constraint:
    model.addCons(quicksum(r[a]*x[a] for a in arcs) <= l)

    """define objective"""
    model.setObjective(quicksum(c[a]*x[a] for a in arcs), "minimize")

    model.data = x, r
    return model


def create_path(x, start):
    """
    Creates a feasible path from the output of
    the SCIP optimization in the form of an array
    """

    arcs = []

    for j in x:
        if model.getVal(x[j]) == 1:
            arcs.append(j)

    path = []
    path.append(start)

    for i in range(len(arcs)):
        for arc in arcs:
            if arc[0] == path[-1]:
                path.append(arc[1])
                arcs.remove(arc)
                pass

    return path


def consumption(model, G, x, r):
    """
    Returns the cost of the RCSP
    """
    arcs = G.arcs()
    return int((sum(r[a]*model.getVal(x[a]) for a in arcs)))


if __name__ == "__main__":
    term_size = os.get_terminal_size()

    dirname = os.path.dirname(__file__)
    instances = ["data/graph1_2.txt",
                 "data/graph4_2.txt",
                 "data/grid1.txt",
                 "data/grid2.txt"]
    # instances = ["data/graph4_2.txt"]
    params = {
            "data/graph1_2.txt": [1, 8, 11],
            "data/graph4_2.txt": [7743, 5983, 280],
            "data/grid1.txt": [0, 16, 357],
            "data/grid2.txt": [0, 100001, 44308]
    }

    for inst in instances:
        print("\n"+"=" * (term_size.columns-1))
        print("Solving RCSPP for:", inst[5:], ":\n")

        start = time.process_time()

        arc_list = os.path.join(dirname, inst)

        G = DiGraph(arc_list)
        s, t, l = params[inst][0], params[inst][1], params[inst][2]

        model = rcspp(G, s, t, l)
        model.hideOutput()  # silent mode
        model.optimize()

        solvetime = model.getSolvingTime()
        x, r = model.data
        opt_val = int(model.getObjVal())

        path = create_path(x, s)
        cons = consumption(model, G, x, r)

        runtime = time.process_time() - start

        print("\nA shortest " + str(s) + "-" + str(t)
              + "-path with resource consumption ≤", l, "is\n", path)
        print("with length", opt_val, "and resource consumption", cons, ".")
        print("The computation took ", "%.1f" % runtime, "seconds of which",
              "%.1f" % solvetime, "seconds were used to solve the model.")
