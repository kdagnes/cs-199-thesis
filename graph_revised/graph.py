import numpy as np
from sympy import Abs, Symbol
import sys

class Vertex:
	def __init__(self, node, node_type, rbs):
		self.id = node
		self.type = node_type #'b' - boundary,'e' - entity,'c' - controller
		self.rbs = rbs
		self.in_arcs = []
		self.out_arcs = []
	
	def __str__(self):
		return "ID:" + str(self.id) + " Type:" + str(self.type)
	def setRBS(self):
		self.rbs = 1
	def getID(self):
		return self.id
	def addInArc(self,arc):
		self.in_arcs.append(arc)
	def addOutArc(self,arc):
		self.out_arcs.append(arc)
	def getInArc(self):
		return self.in_arcs
	def getOutArc(self):
		return self.out_arcs

class Arc:
	def __init__(self, edge, fromNode, toNode, constraint, limit):
		self.id = edge	#string
		self.fromNode = fromNode #vertex
		self.toNode = toNode #vertex
		self.constraint = constraint #string
		self.limit = limit #integer
		self.time = [0] * limit
		
	def __str__(self):
		return str(self.id)
		
	def getArc(self):
		return self.id
		
	def getConstraint(self):
		return self.constraint
	
	def getLimit(self):
		return self.limit
		
	def getFromNode(self):
		return self.fromNode
		
	def getToNode(self):
		return self.toNode

	def getToNodeID(self):
		return self.toNode.getID()

	def possibleTraversal(self):
		if(0 not in self.time):
			return 0
		else:
			return 1

	def checkIfTraversed(self):
		if (self.time[0] != 0):
			return 1
		return 0

	def updateTime(self, time_traversed):
		self.time[self.time.index(0)] = time_traversed
	

class RDLT:
	def __init__(self):
		self.vertices = {} #dictionary
		self.arcs = {}	#dictionary
		self.num_vertices = 0
		self.num_arcs = 0
		start_vertex = 0
		sink_vertex = 0

	def __str__(self):
		return "Vertices:" + str(self.num_vertices) +" Arcs:" + str(self.num_arcs) 
		
	def addVertex(self, node, type, rbs):
		self.vertices[node] = Vertex(node, type, rbs)
		self.num_vertices += 1
	
	#return Vertex object
	def getVertex(self, node):
		return self.vertices[node]

	def getVertices(self):
		return self.vertices

	def getArcs(self):
		return self.arcs
	
	def addArc(self, edge, fromNode, toNode, constraint, limit):
		if(edge in self.arcs.keys()):
			return 0
		if((fromNode not in self.vertices.keys()) or (toNode not in self.vertices.keys())):
			return 0

		from_vertex = self.vertices[fromNode]
		to_vertex = self.vertices[toNode]
		arc = Arc(edge, from_vertex, to_vertex, constraint, limit)
		self.arcs[edge] = arc
		from_vertex.out_arcs.append(arc)
		to_vertex.in_arcs.append(arc)
		self.num_arcs += 1

		return 1

	#return Arc object
	def getArc(self, edge):
		return self.arcs[edge]

	def getStartVertex(self):
		return self.start_vertex

	def setStartVertex(self, start_vertex):
		self.start_vertex = self.vertices[start_vertex]
		

def createRDLT(vertices, vertex_types, rbs, arcs, phi, omega):	
	rdlt = RDLT()
	for v_id in range(0, len(vertices)):
		rdlt.addVertex(vertices[v_id], vertex_types[v_id], rbs[v_id])

	for arc_id, arc in enumerate(arcs):
		vertex = arc.split("_")
		success = rdlt.addArc(arc, vertex[0], vertex[1], omega[arc_id], phi[arc_id])
		if (success == 0):
			print ("Unsuccessful creation of arc")
			return 0
	return rdlt


#For all ingoing arcs to a certain vertex check if they are type-alike
#	If they are type-alike: check if they have different constraints
#	If they have different constraints, add the vertex to the lists of PODs
# 	This method returns the vertex object list of PODs 
def getPointOfDelayList(vertices):
	POD = []
	for vertex in vertices:
		if checkIfPointOfDelay(vertex) == 1:
			POD.append(vertex)

	return POD

def checkIfPointOfDelay(vertex):
	for in_arc in vertex.getInArc():
		for another_arc in vertex.getInArc():
			if in_arc.getConstraint() != another_arc.getConstraint():
				return 1
	return 0

# A path from the start_vertex to the destination_vertex
def getElementaryPaths(destination_vertex_id, path, paths=[]):
	vertex = path[-1]
	#print(vertex)
	if vertex.getID() == destination_vertex_id:
		paths.append(path)
	else:
		for arc in vertex.getOutArc():
			if (arc.getToNode() not in path[:-1]):
				new_path = path + [arc.getToNode()]
				paths = getElementaryPaths(destination_vertex_id, new_path, paths)

	return paths



def getAntecedentSet(start_vertex, destination_vertex):
	paths = getElementaryPaths(destination_vertex.getID(), [start_vertex], [])
	antecendent_set = set()
	for path in paths:
		for vertex in path:
			antecendent_set.add(vertex)
	return antecendent_set

def getConsequentSet(start_vertex, antecendent_set):
	consequent_set = set()
	for in_arc in start_vertex.getInArc():
		vertex = in_arc.getFromNode()
		if vertex in antecendent_set:
			paths = getElementaryPaths(vertex.getID(), [start_vertex], [])
			for path in paths:
				for vertex in path:
					consequent_set.add(vertex)

	return consequent_set - antecendent_set

def getLoopingArcs(antecendent_set, consequent_set, arcs):
	looping_arcs = []
	for arc in arcs:
		if ((arc.getFromNode() in consequent_set) and (arc.getToNode() in antecendent_set)):
			looping_arcs.append(arc)

	return looping_arcs

#check if a path exists from the start vertex to all vertices
def checkIfConnected(rdlt):
	connected_vertices = getConnectedVertices(rdlt.getStartVertex())
	#for vertex in rdlt.getVertices().values():
	 	
	if (all(vertex in connected_vertices) for vertex in rdlt.getVertices().values()):
		return 1
	else:
		return 0

#gets all vertices that is connected from the start vertex through dfs
def getConnectedVertices(start_vertex, vertices=set()):
	vertices.add(start_vertex)
	for arc in start_vertex.getOutArc():
		if arc.getToNode() not in vertices:
			vertices = getConnectedVertices(arc.getToNode(), vertices)

	return vertices

def checkIfNSC(rdlt, start_vertex):
	if (not (checkIfConnected(rdlt))):
		return 0
	point_of_delay_list = getPointOfDelayList(rdlt.getVertices().values())
	looping_arcs = set()
	for vertex in point_of_delay_list:
		antecendent_set = getAntecedentSet(start_vertex, vertex)
		consequent_set = getConsequentSet(vertex, antecendent_set)
		looping_arcs.update(getLoopingArcs(antecendent_set, consequent_set, rdlt.getArcs().values()))
	#case 1:check if possible traversal
	#case 2:check if there exists an arc blabla using defn
	for looping_arc in looping_arcs:
		if (looping_arc.getConstraint() != Symbol("EPSILON", positive=True)):
			vertex = looping_arc.getToNode()
			other_arcs = vertex.getInArc()
			other_arcs.remove(looping_arc)
			same_constraint = 0
			for arc in other_arcs:
			 	if arc.getConstraint() == looping_arc.getConstraint():
			 		same_constraint += 1 
			if(same_constraint == 0):
				return 0
	return 1	

#Input the RDLT
rdlt_file = open(sys.argv[1], 'r')

vertices = rdlt_file.readline().split()
vertex_types = rdlt_file.readline().split()
rbs = rdlt_file.readline().split()
rbs = [int(i) for i in rbs]
arcs = rdlt_file.readline().split()
phi = rdlt_file.readline().split()
phi=np.array([int(i) for i in phi])
omega = rdlt_file.readline().split()
omega =np.array([Symbol(i, positive=True) for i in omega])

rdlt = createRDLT(vertices, vertex_types, rbs, arcs, phi, omega)
print (rdlt)

rdlt.setStartVertex("w")

print ("start_vertex:")
print (rdlt.getStartVertex())
point_of_delay_list = getPointOfDelayList(rdlt.getVertices().values())
paths = getElementaryPaths(rdlt.getVertex('x8').getID(),[rdlt.getVertex('w')],[])

# for path in paths:
# 	print ("PATH")
# 	for vertex in path:
# 		print(vertex)

print("Connected Vertices")
vertices = getConnectedVertices(rdlt.getVertex('w'), set())
for vertex in vertices:
	print (vertex)

checkIfConnected(rdlt)

antecendent_set = getAntecedentSet(rdlt.getVertex('w'), rdlt.getVertex('x8'))
print ("antecendent_set of x8")
for vertex in antecendent_set:
	print (vertex)

print ("consequent_set of x8")
consequent_set = getConsequentSet(rdlt.getVertex('x8'),antecendent_set)
for vertex in consequent_set:
	print (vertex)

looping_arcs = getLoopingArcs(antecendent_set, consequent_set, rdlt.getArcs().values())
print ("looping_arcs used by x8")
for arc in looping_arcs:
	print (arc)

nsc = checkIfNSC(rdlt, rdlt.getVertex('w'))
if (nsc == 1):
	print ("The RDLT is NSC. Therefore, the RDLT is also C-verifiable.")
else:
	print ("The RDLT is not NSC. It is also not C-verifiable.")
