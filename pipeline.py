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

ouputFolder = "resource"

for epara in params:
    call([  "python", "graph.py",
            "-l", str(epara.energy[0]),
            "-u", str(epara.energy[1]),
            "-n", str(epara.nnode),
            "-e", str(epara.nedge),
            "-o", ouputFolder + "/" + epara.outputEdge,
            "-p", ouputFolder + "/" + epara.outputPickle
        ])
