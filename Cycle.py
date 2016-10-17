from sets import Set
from graph import *
import math

EPS = 0.01

class Cycle(object):

    def __init__(self):
        self.edges = []

    def __iter__(self):
        return iter(self.edges)

    def addEdge(self, edge):
        self.edges.append(edge)

    def __len__(self):
        return len(self.edges)

    def __str__(self):
        return str(self.edges)

    def __repr__(self):
        return str(self)

    def reorder(self):

        origin = set(self.edges)
        final = set([])

        begin = origin.pop()
        final.add(begin)

        vertex = begin.to

        while len(origin) > 0:

            popItem = None
            appendItem = None

            for edge in origin:

                if edge.fr == vertex:

                    # good order
                    vertex = edge.to
                    popItem = edge
                    appendItem = edge
                    break

                elif edge.to == vertex:

                    vertex = edge.fr
                    popItem = edge
                    appendItem = Edge(edge.to, edge.fr)
                    break

            origin.remove(popItem)
            final.add(appendItem)

        self.edges = list(final)

    def consistency(self, graph):
        val = 0

        for edge in self.edges:

            weight = graph.getWeightWithEdge(edge)
            val += weight

        return val

class CycleTracker(object):

    def __init__(self):
        self.cycles = []

    def __iter__(self):
        return iter(self.cycles)

    def addCycle(self, cycle):
        self.cycles.append(cycle)

    def __len__(self):
        return len(self.cycles)

class EdgeTracker(object):

    def __init__(self):
        self.edges = []
        self.goods = set([]) # set of perfect edges
        
        # mapping edge --> counter
        self.bads = {}

    def getEdge(self, idx):
        return self.edges[idx]

    def addEdge(self, edge):
        self.edges.append(edge)

    def addGoodEdge(self, edge):
        self.goods.add(edge)

    def addBadEdge(self, edge):
        if edge not in self.bads:
            self.bads[edge] = 0
        self.bads[edge] += 1

    def isGoodEdge(self, edge):
        return edge in self.goods

    def isBadEdge(self, edge):
        return edge in self.bads

def isGoodWeightedCycle(graph, cycle):
    """
        If weighted less than some threshold, its considered
        good cycle and every edges in its cycle should be
        a good cycle two.
    """
    return math.fabs(cycle.consistency(graph)) < EPS

"""
Algorithm:
- Step 1: Loop through each cycle, if cycle is good
add all edge into good edge. If its bad cycle, put
it into a list of "bad" cycles

- Step 2: Loop through each "bad" cycle, for every
edge in bad cycle, if that edge not in the good list
, put it into the bad list, it can keep a counter.

- Step 3: Return a list of bad edge, sorted

"""

# edge1 = WeightedEdge(0, 1, 15.0)
# edge2 = WeightedEdge(2, 3, 15.4)
# cycle1 = WeightedCycle()
# cycle1.addEdge(edge1)
# cycle1.addEdge(edge2)

def readCycleMatrix(filename, orders):
    # it will return a list of cycle
    # with mapping from the orders

    """
    Idea:


    """

    cycles = []

    lines = [line.rstrip(' \n') for line in open(filename)]

    for line in lines:
        cycle = Cycle()

        res = line.split(" ")

        for idx, val in enumerate(res):
            # if cycle contains this edge
            if int(val) == 1:
                cycle.addEdge(orders[idx])

        cycle.reorder()
        cycles.append(cycle)

    return cycles


def readEdgeOrder(filename):

    lines = [line.rstrip('\n') for line in open(filename)]

    orders = []

    for line in lines:
        res = line.split(" ")

        fr = int(res[0])
        to = int(res[1])

        edge = Edge(fr, to)
        orders.append(edge)

    return orders

def getSortedListBadEdges(graph, cycles):

    badCycles = []

    edgeTrker = EdgeTracker()

    # STEP 1
    for cycle in cycles:

        # if it is a good cycle
        if isGoodWeightedCycle(graph, cycle):

            # put all good edge into tracker
            for edge in cycle:
                edgeTrker.addGoodEdge(edge)

        else:
            badCycles.append(cycle)

    # STEP 2

    # for each bad cycle
    for cycle in badCycles:

        # each edge in the cycle
        for edge in cycle:

            # if it is not a good edge
            # it can be a bad edge
            if not edgeTrker.isGoodEdge(edge):
                edgeTrker.addBadEdge(edge)

    print(edgeTrker.bads)

if __name__ == "__main__":
    # get the list of edges from the file
    orders = readEdgeOrder("order.txt")
    cycles = readCycleMatrix("matrix.txt", orders)
    graph = Graph.loadAsPickleInFile("out.pkl")

    graph.printInfo()

    # update 1 -> 8
    graph.updateEdge(1, 8, -11.0)
    graph.updateEdge(2, 3, -3.0)

    getSortedListBadEdges(graph, cycles)
    





