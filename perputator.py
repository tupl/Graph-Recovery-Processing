"""
    The purpose of this one is to randomly perpuate an edge in a graph
"""
from graph import *

class GraphPerputator(object):

    def __init__(self, small, large):
        self.small = small
        self.large = large

    def execute(self, graph, percent):

        small = self.small
        large = self.large
        err = []

        print("Perputating the graph")
        for fr in graph.adjList:
            for to in graph.adjList[fr]:
                prob = random.random()
                val = 0
                # how many percent random large
                if prob <= percent:
                    val = random.uniform(large[0], large[1])
                else:
                    val = random.uniform(small[0], small[1])
                err.append(val)
                graph.shiftEdge(fr, to, val)

        import numpy as np

def strToTuple(strTuple):
    ret = strTuple.split(",")
    first = int(ret[0])
    second = int(ret[1])
    return (first, second)

def main(args):
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
            percent = int(arg)
    try:
        graph = Graph.loadAsPickleInFile(inputGraph)
        perputator = GraphPerputator(good, bad)
        perputator.execute(graph, percent)
    except err:
        print(err)

if __name__ == "__main__":
    main(sys.argv[1:])
