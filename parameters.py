"""
Author: tuleph@gmail.com

Goal: The purpose of this code is to contain all parameters to execute the
    whole pipeline

"""

class Param(object):

    def __init__(self, energy, nnode, nedge, outputEdge, outputPickle):
        self.energy = energy
        self.nnode = nnode
        self.nedge = nedge
        self.outputEdge = outputEdge
        self.outputPickle = outputPickle

params = [
    Param((10, 40), 10, 25, "10_25-1.grp", "10_25-1.pkl"),
    Param((10, 40), 10, 25, "10_25-2.grp", "10_25-2.pkl"),
    Param((10, 40), 10, 25, "10_25-3.grp", "10_25-3.pkl"),

    Param((10, 40), 20, 50, "20_50-1.grp", "20_50-1.pkl"),
    Param((10, 40), 20, 50, "20_50-2.grp", "20_50-2.pkl"),
    Param((10, 40), 20, 50, "20_50-3.grp", "20_50-3.pkl"),

    Param((10, 40), 40, 100, "40_100-1.grp", "40_100-1.pkl"),
    Param((10, 40), 40, 100, "40_100-2.grp", "40_100-2.pkl"),
    Param((10, 40), 40, 100, "40_100-3.grp", "40_100-3.pkl")
]
