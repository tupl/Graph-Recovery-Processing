"""
    The purpose of this one is to randomly perpuate an edge in a graph
"""
from graph import *
from util import *

import sys, getopt

class GraphPerputator(object):

    def __init__(self, small, large):
        self.small = small
        self.large = large

    def execute(self, graph, percent):

        small = self.small
        large = self.large
        err = []

        for fr in graph.adjList:
            for to in graph.adjList[fr]:
                prob = random.random()
                val = 0
                # how many percent random large
                if prob <= percent:
                    val = random.uniform(large[0], large[1])
                else:
                    val = random.uniform(small[0], small[1])

                # add negative or positive
                prob = random.random()
                if prob < 0.5:
                    val = -val;

                err.append(val)
                graph.shiftEdge(fr, to, val)

        import numpy as np

def main(argv):
    """
        -i input file
        -g, --good (low, high)
        -b, --bad (low, high)
        -o output list of bad edges
        -p output the picke holding new graph
        -t percent of bad edges
    """

    good = (0, 2)
    bad = (10, 20)
    percent = 0.3

    inputGraph = ""

    outputEdge = "edge.grp"
    outputPickle = "out.pkl"

    try:
        opts, args = getopt.getopt(argv,"hi:g:b:o:p:t:"
            ,[  "help"
                "good=",
                "bad=",
                "outputEdge=",
                "outputPickle"])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.exit()
        elif opt in ("-i"):
            inputGraph = arg
        elif opt in ("-g", "--good"):
            good = strToTuple(arg)
        elif opt in ("-b", "--bad"):
            bad = strToTuple(arg)
        elif opt in ("-o", "--outputEdge"):
            outputEdge = arg
        elif opt in ("-p", "--outputPickle"):
            outputPickle = arg
        elif opt in ("-t"):
            percent = float(arg)
    try:
        print("Loaded the graph from " + inputGraph)
        graph = Graph.loadAsPickleInFile(inputGraph)
        perputator = GraphPerputator(good, bad)

        print("Start perputating the graph")
        perputator.execute(graph, percent)
        print("Finish perputating the graph")

        # save graph into destination
        graph.saveAsPickleInFile(outputPickle)
        print("Saved the graph to " + outputPickle)

    except Exception as err:
        print(err)

if __name__ == "__main__":
    main(sys.argv[1:])
