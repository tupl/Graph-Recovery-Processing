from sets import Set
import random

class Node(object):

	def __init__(self, id, energy, name=None):
		self.id = id
		self.name = name
		self.energy = energy

	def __str__(self):
		return str(self.id) + "[" +  str(self.energy) + "]"

class GraphInfo(object):

	def __init__(self):
		self.numberNodes = 0
		self.energy = (0, 100)

class Graph(object):
	"""

	"""
	@staticmethod
	def generate(graphInfo):

		graph = Graph()

		low, high = graphInfo.energy

		for time in range(graphInfo.numberNodes):
			energy = random.randint(low, high)
			graph.addNode(energy)

		return graph

	def __init__(self):
		self.nodes = []
		self.adjList = {}

	def getNode(self, id):
		return self.nodes[id]

	def printInfo(self):
		print("Nodes in the graph")

		for n in self.nodes:
			print(n)

		print("Edges in the graph")

		for fr in self.adjList:
			print("AdjList for node " + str(fr))
			print(str(self.adjList[fr]))

	def updateEdge(self, fr, to, weight):
		# update this edge with new weight
		self.adjList[fr][to] = weight

	def getAdjListOfNode(self, fr):
		return self.adjList[fr]

	def getNumberOfNodes(self):
		return len(self.nodes)

	def addEdge(self, fr, to, weight):
		if fr not in self.adjList:
			self.adjList[fr] = {}
		self.adjList[fr][to] = weight

	def addNode(self, energy, name=None):
		nextId = len(self.nodes)
		n = Node(nextId, energy, name)
		self.nodes.append(n)

		return n

def weightEnergy(nodeFr, nodeTo):
	return nodeTo.energy - nodeFr.energy

def getSetRandomlyPick(aset):
	ls = list(aset)
	return random.choice(ls)

class SpaningTreeGenerator(object):
	"""
		It takes a Graph object, and add edge to make it
		become a spanning tree
	"""

	def __init__(self):
		pass

	def generate(self, graph, operator = None):
		"""
		By the default, if it add an edge with weight 0,
		if is has operator, it will ask operator to return
		a weight for two node
			operator(node1, node2) --> weight

		Algorithm:
			- keep track of reachable node and unreachable
			node.
			- at beginning, put node 0 into reachable
			- at any time, we make an edge from
			reachable node to non-reachable node
			- we move the new non-reachable node to reachable node
			- repeat it exactly n - 1 time
		"""
		if graph.getNumberOfNodes() == 0:
			raise Exception("Required at least one node")

		n = graph.getNumberOfNodes()

		print("There are " + str(n) + " nodes in the graph.")

		reachable = Set([0])
		non_reachable = Set([])

		for v in range(1, n):
			# add each node v into non-reachable node
			non_reachable.add(v)

		for time in range(0, n - 1):
			fr = getSetRandomlyPick(reachable)
			to = getSetRandomlyPick(non_reachable)

			reachable.add(to)
			non_reachable.discard(to)

			nodeFr = graph.getNode(fr)
			nodeTo = graph.getNode(to)

			if operator:
				val = operator(nodeFr,nodeTo)
				graph.addEdge(fr, to, val)
			

# graphInfo = GraphInfo()
# graphInfo.energy = (15, 20)
# graphInfo.numberNodes = 25

# myGraph = Graph.generate(graphInfo)

# myGraph.printInfo()

# generator = SpaningTreeGenerator()
# generator.generate(myGraph, weightEnergy)

# myGraph.printInfo()