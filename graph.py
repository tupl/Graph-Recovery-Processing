from sets import Set
import random

class Edge(object):

    def __init__(self, fr, to):
        self.fr = fr
        self.to = to

    def __str__(self):
        return str(self.fr) + " -> " + str(self.to)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.fr, self.to))

    def __eq__(self, other):
        return (self.fr, self.to) == (other.fr, other.to)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other) 

class WeightedEdge(Edge):

    def __init__(self, fr, to, weight):
        super(WeightedEdge, self).__init__(fr, to)
        self.weight = weight

    def __str__(self):
        return str(self.fr) + " -> " + str(self.to) + "[" + str(self.weight) + "]"

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
		Construct a directed graph.
	"""
	@staticmethod
	def generate(graphInfo):

		graph = Graph()

		low, high = graphInfo.energy

		for time in range(graphInfo.numberNodes):
			energy = random.uniform(low, high)
			graph.addNode(energy)

		return graph

	def __init__(self):
		self.nodes = []
		self.adjList = {}
		self.numberEdges = 0

	def getWeightWithEdge(self, edge):
		fr = edge.fr
		to = edge.to

		if fr in self.adjList and to in self.adjList[fr]:
			return self.adjList[fr][to]
		return - self.adjList[to][fr]

	def getNode(self, id):
		return self.nodes[id]

	def isEdgeInGraph(self, fr, to):
		if fr not in self.adjList:
			return False # this edge not in the graph
		return to in self.adjList[fr]

	def printInfo(self):
		print("Nodes in the graph")

		for n in self.nodes:
			print(n)

		print("Edges in the graph")

		for fr in self.adjList:
			print("AdjList for node " + str(fr))
			print(str(self.adjList[fr]))

	@staticmethod
	def loadAsPickleInFile(filename):
		import pickle

		return pickle.load(open(filename, "rb" ))

	def saveAsPickleInFile(self, filename):
		import pickle

		pickle.dump(self, open(filename, "wb"))

	def saveEdgesInFile(self, filename):

		with open(filename, 'w') as fi:
			for fr in self.adjList:
				myNeighbor = self.adjList[fr]
				for to in myNeighbor:
					nstr = str(fr) + " " + str(to) + " " + str(myNeighbor[to])
					fi.write(nstr + "\n")

	def updateEdge(self, fr, to, weight):
		# update this edge with new weight
		self.adjList[fr][to] = weight

	def getAdjListOfNode(self, fr):
		return self.adjList[fr]

	def getNumberOfEdges(self):
		return len(self.numberEdges)

	def getNumberOfNodes(self):
		return len(self.nodes)

	def addEdge(self, fr, to, weight):
		if fr not in self.adjList:
			self.adjList[fr] = {}
		if to not in self.adjList[fr]:
			# we add a new edge
			self.numberEdges += 1
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

class EdgeAppendGenerator(object):

	def generate(self, graph, numberEdges):
		"""
			How many edge you want to add to this graph

		"""

		idx = 0

		numberNodes = graph.getNumberOfNodes()
		choices = list(range(numberNodes))

		while idx <= numberEdges:

			# an edge not in graph if its (fr, to) or
			# (to, fr) are not in the graph

			[fr, to] = random.sample(choices, 2)

			stt1 = graph.isEdgeInGraph(fr, to)
			stt2 = graph.isEdgeInGraph(to, fr)

			if stt1 or stt2:
				# if its is in the graph, ignore this cycle
				continue

			idx += 1

			nodeFr = graph.getNode(fr)
			nodeTo = graph.getNode(to)

			graph.addEdge(fr, to, weightEnergy(nodeFr, nodeTo))


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


if __name__ == "__main__":
	graphInfo = GraphInfo()
	graphInfo.energy = (10, 40)
	graphInfo.numberNodes = 10

	myGraph = Graph.generate(graphInfo)

	# myGraph.printInfo()

	generator = SpaningTreeGenerator()
	generator.generate(myGraph, weightEnergy)

	# print
	# myGraph.printInfo()

	edgeGenerator = EdgeAppendGenerator()
	edgeGenerator.generate(myGraph, 10)

	# print
	myGraph.printInfo()

	myGraph.saveEdgesInFile("out.grp")
	myGraph.saveAsPickleInFile("out.pkl")
