"""
Author: tuleph@gmail.com

Goal: The purpose of this code is to correct the value of edge and evaluate
    the performance

Algorithm:


Commandline Interface:

"""

from sets import Set
from graph import *

import math
import numpy as np
import sys

EPS = 1.0

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

    def exists(self, e):
        for edge in self.edges:
            if edge == e:
                return 1
            elif edge.reverse() == e:
                return -1
        return 0

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

    return badCycles, edgeTrker

def GradientDescent(graph, badCycles, cycles, edgeTrker):

    import copy

    edges = Set([])

    vGraph = copy.deepcopy(graph)
    x_bound = []

    for edge in edgeTrker.bads:
        if edge not in edges and \
            edge.reverse() not in edges:
            edges.add(edge)
            x_min = -2.0 + graph.getWeightWithEdge(edge)
            x_max = 2.0 + graph.getWeightWithEdge(edge)
            x_bound.append((x_min, x_max))

    for edge in edgeTrker.goods:
        if edge not in edges and \
            edge.reverse() not in edges:
            edges.add(edge)
            x_min = -2.0 + graph.getWeightWithEdge(edge)
            x_max = 2.0 + graph.getWeightWithEdge(edge)
            x_bound.append((x_min, x_max))

    X_Error = list(edges)

    n = len(X_Error)
    x_0 = np.zeros((1, n))

    import math

    for idx, edge in enumerate(X_Error):
        x_0[0, idx] = vGraph.getWeightWithEdge(edge)

    def EvaluateFunction(x_):

        for idx, edge in enumerate(X_Error):
            fr = edge.fr
            to = edge.to
            vGraph.updateEdge(fr, to, x_[idx])

        nCycles = len(cycles)

        err = np.zeros((1, nCycles))

        for idx, cycle in enumerate(cycles):
            err[0, idx] = cycle.consistency(vGraph)

        err_val = np.dot(err, err.T)

        return math.log(2 + err_val[0][0])

    from scipy import optimize

    times = 0

    while times < 10:
        print("Iteration %d" % times)

        x_val, nfeval, rc = optimize.fmin_tnc(
            EvaluateFunction, x_0,
            approx_grad = True,
            bounds = x_bound,
            disp = 0,
            maxfun = 1000
        )

        x_0 = x_val
        times += 1

    ret = []

    for idx, edge in enumerate(X_Error):
        e = WeightedEdge(edge.fr, edge.to, x_val[idx])
        ret.append(e)

    return ret


def LeastSquareInitPoint(graph, badCycles, cycles, edgeTrker, includeGood=False):
    """
        It requires graph & edgeTrker to recover
    Procedure
        Phase 1: Adding all bad edges into a list of edges to consider
                 (We will add good edges too if we set includeGood)

        Phase 2:
    """

    b = []
    X = []

    edges = Set([])

    for edge in edgeTrker.bads:
        if edge not in edges and \
            edge.reverse() not in edges:
            edges.add(edge)

    if includeGood:
        for edge in edgeTrker.goods:
            if edge not in edges and \
                edge.reverse() not in edges:
                edges.add(edge)

    # Convert the edges into a list
    X_Error = list(edges)

    n = len(X_Error) # n edges
    m = len(badCycles) # m cycles

    A = np.zeros((m, n))
    b = np.zeros((m, 1))

    np.set_printoptions(threshold=np.inf)

    # Setting up matrix A
    for row, cycle in enumerate(badCycles):

        # for each edge in X
        for col, edge in enumerate(X_Error):

            val = cycle.exists(edge)
            A[row, col] = val

        b[row, 0] = cycle.consistency(graph)


    # x_Solu, residuals, rank, s = np.linalg.lstsq(A, b, 5.0)

    import scipy
    from scipy import linalg
    x_Solu, residuals, rank, s = linalg.lstsq(A, b, lapack_driver = "gelss")

    ret = []

    for idx, edge in enumerate(X_Error):
        weight = graph.getWeightWithEdge(edge) - x_Solu[idx]
        e = WeightedEdge(edge.fr, edge.to, weight[0])
        ret.append(e)

    return ret

class GraphEvaluator(object):

    def getError(self, graph, edges):

        n = len(edges)

        OriErr = np.zeros((1, n))
        PredErr = np.zeros((1, n))

        print("====================")
        print("Summary of statistics of error")
        for col, edge in enumerate(edges):

            # Information about node
            fr = edge.fr
            to = edge.to

            pred = edge.weight
            ori = graph.getWeightWithEdge(Edge(fr, to))

            # Expected Value
            real = weightEnergy(graph.getNode(fr),
                graph.getNode(to))

            OriErr[0, col] = ori - real
            PredErr[0, col] = pred - real

        print("====================")
        print("Original Error")
        print("Mean Error = %f" % np.mean(OriErr))
        print("Std Error = %f" % np.std(OriErr))
        print("Max Error = %f" % np.amax(np.absolute(OriErr)))

        print("====================")
        print("Predicted Error")
        print("Mean Error = %f" % np.mean(PredErr))
        print("Std Error = %f" % np.std(PredErr))
        print("Max Error = %f" % np.amax(np.absolute(PredErr)))

def histogramCycle(cycles):
    counter = {}

    for cycle in cycles:
        cycleLen = len(cycle)

        if cycleLen not in counter:
            counter[cycleLen] = 0

        counter[cycleLen] += 1

    return counter

def filterCycle(cycles, threshold):
    ret = []

    for cycle in cycles:
        if len(cycle) <= threshold:
            ret.append(cycle)

    return ret

if __name__ == "__main__":
    """

    """
    graphPath = sys.argv[1]
    orderPath = sys.argv[2]
    cyclesPath = sys.argv[3]

    EPS = 2.0

    # get the list of edges from the file
    orders = readEdgeOrder(orderPath)
    cycles = readCycleMatrix(cyclesPath, orders)
    graph = Graph.loadAsPickleInFile(graphPath)

    cycleHist = histogramCycle(cycles)
    cycleThreshold = 7

    print
    print("===== ===== ===== ===== =====")
    print("File name : " + graphPath)
    print("Dicarding all cycles greater than " + str(cycleThreshold))
    cycles = filterCycle(cycles, cycleThreshold)

    # get a list of bad cycles in the graph
    badCycles, edgeTrker = getSortedListBadEdges(graph, cycles)

    print
    print("Current threshold = " + str(EPS))
    print("Original number of cycles = " + str(len(cycles)))
    print("Predicted number of bad cycles = " + str(len(badCycles)))

    print
    numberBadEdges = len(edgeTrker.bads)
    totalEdges = graph.numberEdges
    print("This result only includes error coming from predicted bad edges.")
    print("Total number of nodes = " + str(graph.getNumberOfNodes()))
    print("Number of bad edges found = " + str(numberBadEdges))
    print("Total Number of edges = " + str(totalEdges))
    print("Percentage = " + str(numberBadEdges * 100.0 / totalEdges))
    print

    # using least square
    pred_edges = LeastSquareInitPoint(graph, badCycles, cycles, edgeTrker, includeGood=False)
    evaluator = GraphEvaluator()
    evaluator.getError(graph, pred_edges)

    # pred_edges = LeastSquareInitPoint(graph, badCycles, cycles, edgeTrker, includeGood = True)
    # evaluator = GraphEvaluator()
    # evaluator.getError(graph, pred_edges)

    # for idx, edge in enumerate(pred_edges):
    #     fr = edge.fr
    #     to = edge.to
    #     graph.updateEdge(fr, to, edge.weight)

    # using gradient GradientDescent
    # pred_edges = GradientDescent(graph, badCycles, cycles, edgeTrker)
    # evaluator = GraphEvaluator()
    # evaluator.getError(graph, pred_edges)
