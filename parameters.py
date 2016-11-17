"""
Author: tuleph@gmail.com

Goal: The purpose of this code is to contain all parameters to execute the
    whole pipeline

"""

class GraphParam(object):

    def __init__(self, energy, nnode, nedge, outputEdge, outputPickle):
        self.energy = energy
        self.nnode = nnode
        self.nedge = nedge
        self.outputEdge = outputEdge
        self.outputPickle = outputPickle

class PerputatingParam(object):

    def __init__(self, good, bad, percent, inputFile, outputFile):
        self.good = good
        self.bad = bad
        self.percent = percent
        self.inputFile = inputFile
        self.outputFile = outputFile

params = [
    GraphParam((10, 40), 10, 25, "10_25-1.grp", "10_25-1.pkl"),
    GraphParam((10, 40), 10, 25, "10_25-2.grp", "10_25-2.pkl"),
    GraphParam((10, 40), 10, 25, "10_25-3.grp", "10_25-3.pkl"),

    GraphParam((10, 40), 20, 50, "20_50-1.grp", "20_50-1.pkl"),
    GraphParam((10, 40), 20, 50, "20_50-2.grp", "20_50-2.pkl"),
    GraphParam((10, 40), 20, 50, "20_50-3.grp", "20_50-3.pkl"),

    GraphParam((10, 40), 40, 100, "40_100-1.grp", "40_100-1.pkl"),
    GraphParam((10, 40), 40, 100, "40_100-2.grp", "40_100-2.pkl"),
    GraphParam((10, 40), 40, 100, "40_100-3.grp", "40_100-3.pkl")
]

perparams = [
    PerputatingParam((0, 2), (10, 20), 0.3, "10_25-1.pkl", "10_25-1.pkl"),
    PerputatingParam((0, 2), (10, 20), 0.3, "10_25-2.pkl", "10_25-2.pkl"),
    PerputatingParam((0, 2), (10, 20), 0.3, "10_25-3.pkl", "10_25-3.pkl"),

    PerputatingParam((0, 2), (10, 20), 0.3, "20_50-1.pkl", "20_50-1.pkl"),
    PerputatingParam((0, 2), (10, 20), 0.3, "20_50-2.pkl", "20_50-2.pkl"),
    PerputatingParam((0, 2), (10, 20), 0.3, "20_50-3.pkl", "20_50-3.pkl"),

    PerputatingParam((0, 2), (10, 20), 0.3, "40_100-1.pkl", "40_100-1.pkl"),
    PerputatingParam((0, 2), (10, 20), 0.3, "40_100-2.pkl", "40_100-2.pkl"),
    PerputatingParam((0, 2), (10, 20), 0.3, "40_100-3.pkl", "40_100-3.pkl"),
]
