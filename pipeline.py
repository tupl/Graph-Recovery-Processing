"""
Author: tuleph@gmail.com

Goal: This script's purpose is to construct a pipeline

Pipeline:
    -- Generating a synthetic graph

    -- Randomly perputating edge in graph

    -- Correcting the synthetic graph

Commandline Interface:

"""

from parameters import *
from subprocess import call
from util import *

graphPath = "resource"
perputatingPath = "perputation"
cyclePath = "cycles"

def GraphCyclePhase():
    for epara in cycparams:
        call([  "java", "-jar", "CycleFinder.jar",
                graphPath + "/" + epara.inputFile,
                cyclePath + "/" + epara.outputOrder,
                cyclePath + "/" + epara.outputCycle,
                str(epara.minCycle),
                str(epara.maxIteration)
            ])

def GraphPerputatorPhase():
    for epara in perparams:
        call([  "python", "perputator.py",
                "-i", graphPath + "/" + epara.inputFile,
                "-g", tupleToStr(epara.good),
                "-b", tupleToStr(epara.bad),
                "-t", str(epara.percent),
                "-p", perputatingPath + "/" + epara.outputFile
            ])

def GraphEvaluator():
    for epara in evalparams:
        call([  "python", "Cycle.py",
                perputatingPath + "/" + epara.graph,
                cyclePath + "/" + epara.order,
                cyclePath + "/" + epara.matrix
            ])

def GraphGeneratePhase():
    for epara in params:
        call([  "python", "graph.py",
                "-l", str(epara.energy[0]),
                "-u", str(epara.energy[1]),
                "-n", str(epara.nnode),
                "-e", str(epara.nedge),
                "-o", graphPath + "/" + epara.outputEdge,
                "-p", graphPath + "/" + epara.outputPickle
            ])



if __name__ == "__main__":
    # GraphGeneratePhase()
    # GraphCyclePhase()
    # GraphPerputatorPhase()
    GraphEvaluator()
