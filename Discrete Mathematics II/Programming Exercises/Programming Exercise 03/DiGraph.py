import numpy as np
from tqdm import tqdm

# Class to represent directed graphs:

  # This class can be initialized without input arguments. Otherwise it
  # takes files in the same format as graph1.txt provided on the whiteboardpage
  # of this course in the KVV.
class DiGraph:
    def __init__(self, arc_list = None):
        # Arc-list that contains lists with 4 entries: [tail: int, head: int, weight: float, resource: float].
        self.A = []
        if arc_list != None:
            file = open(arc_list, "r")
            arc_dat = file.readlines()
            for k in range(2,len(arc_dat)):
                a = arc_dat[k].split(";")
                arc_in = [int(a[0]), int(a[1]), float(a[2]), float(a[3])]
                self.A.append(arc_in)

  # Function that returns a list containing all the nodes in G
    def V(self):
        V = set()
        for a in self.A:
            V.add(a[0])
            V.add(a[1])
        return list(V)
  
  # Function returns a list that saves the index of the first occurence in the 
  # list E of an arc with tail u at the index u - assumes that E is a forward
  # star arc list
    def pointers(self):
        pointers = [None]*(max(self.V()))
        # Iterates through all arcs.
        for counter in range(0, len(self.A)):
        # self.A[counter][0] is the tail of the arc at the index: counter in the arc-list. Before the first occurence of a
        # node v as tail the entry pointers[v-1] is None and will be set to counter (index of the first occurence in the arc-list).
            if pointers[self.A[counter][0]-1] == None:
                pointers[self.A[counter][0]-1] = counter
        return pointers

  # Function to determine the nodes adjacent to the input node. Returns list of outgoing arcs from u.
    def neighbors(self, u, pointers = None):
        # Node v corresponds to index v-1.
        v = u - 1
        # Case pointers list was provided:
        if pointers != None:
            # Case: u has outgoing arcs.
            if pointers[v] != None:
                first = pointers[v]
                # Last is the index of the next node, i.e. last-1 is the last index such that G.A[last-1] is an outgoing arc from u.
                last = None
                step = 0
                # Last is updated when an outgoing arc from a different node appears in the arc-list.
                while last == None and v + step < len(pointers)-1:
                    step += 1
                    last = pointers[v+step]
                # Case: u is the last tail => last is the last index of the arc-list.
                if last == None:
                    last = len(self.A)-1
                # Case: first and last are defined.
                return self.A[first:last]
            # Case: first and last are not defined => returns empty list.
            return []
        retval = []
        # Case: pointers-list was not provided.
        for a in self.A:
            if e[0] == u:
                retval.append(e)
        return retval

    def resources(self):
        r = {}
        for arc in self.A:
            name = (arc[0], arc[1])
            r[name] = arc[3]

        return r

    def costs(self):
        c = {}
        for arc in self.A:
            name = (arc[0], arc[1])
            c[name] = arc[2]

        return c

    def arcs(self):
        arcs = []
        for arc in self.A:
            arcs.append((arc[0], arc[1]))

        return arcs


    def in_out_arcs(self):
        arcs = self.A
        nodes = self.V()
        in_arcs = {node: [] for node in nodes}
        out_arcs = {node: [] for node in nodes}

        for u in tqdm(nodes, desc="Generating arc dictionary     "):
            for a in arcs:
                arc = (a[0], a[1])
                if a[0] == u:
                    out_arcs[u].append(arc)
                elif a[1] == u:
                    in_arcs[u].append(arc)
                else:
                    pass

        return in_arcs, out_arcs
    

    """
    EXPERIMENTAL:

    def in_out_arcs(self):
        arcs_in, arcs_out = [], []
        nodes = self.V()
        in_arcs = {node: [] for node in nodes}
        out_arcs = {node: [] for node in nodes}

        for arcs in self.A.copy():
            arcs_in.append((arcs[0], arcs[1]))
            arcs_out.append((arcs[0], arcs[1]))

        for u in tqdm(nodes, desc="Generating arc dictionary"):
            for a in arcs_out:
                if a[0] == u:
                    out_arcs[u].append(a)

            for a in arcs_in:
                if a[1] == u:
                    in_arcs[u].append(a)

            for a in arcs_in:
                for b in in_arcs[u]:
                    if b == a:
                        arcs_in.remove(a)

            for a in arcs_out:
                for b in out_arcs[u]:
                    if b == a:
                        arcs_out.remove(a)

        return in_arcs, out_arcs
        """


