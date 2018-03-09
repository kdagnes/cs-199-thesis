#This code implements the graphical representation of an RDLT
#This takes in an RDLT input and an acitvity profile with the start and final vertices
#This checks the validity, verifiability of an activity profile
#This checks the soundness property of an RDLT given an activity profile


class Vertex:
	def __init__(self, node, node_type, rbs):
		self.id = node
		self.type = node_type #'b' - boundary,'e' - entity,'c' - controller
		self.rbs = rbs
		self.in_arcs = []
		self.out_arcs = []
	
	def __str__(self):
		return "ID:" + str(self.id) + " Type:" + str(self.type)
	
	

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
		
	def fromNode(self):
		return self.fromNode
		
	def toNode(self):
		return self.toNode

	def lessenLimit(self):
		self.limit -= 1
		return

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
		
	def addVertex(self, node, type, rbs):
		self.vertices[node] = Vertex(node, type, rbs)
		self.num_vertices += 1
	
	#return Vertex object
	def getVertex(self, node):
		return self.vertices[node]
	
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
		
	
def validifyActivityProfile (rdlt, activity_profile, start_vertex, final_vertex):
	#check if first config arcs contain start vertex
	for arc in activity_profile[0]:
		if (arc[0] != start_vertex):
			print("Invalid start vertex")

	#check if last config arcs contain end vertex
	for arc in activity_profile[-1]:
		if (arc[1] != final_vertex):
			print ("Invalid final vertex")

	#check if each arc is a valid traversal for each config
	for id_config, config in enumerate(activity_profile):
		print ("Reachability Configuration: " + str(id_config+1))
		y_vertices = []

		#check if L-constraint is satisfied
		#and get the goal vertices
		for arc in config:
			if(not(rdlt.arcs[arc[0] + "_" + arc[1]].possibleTraversal())):
				print ("Limit traversal is reached")
				return 0

			rdlt.arcs[arc[0] + "_" + arc[1]].updateTime(id_config+1)

			if(arc[1] not in y_vertices):
				y_vertices.append(arc[1])

		for goal_vertex in y_vertices:
			arc_list = []
			for arc in config:
				if (arc[1] == goal_vertex):
					arc_list.append(arc[0]+"_"+arc[1])
				
			if (checkUnconstrained(rdlt, goal_vertex, arc_list) == 0):
				print ("Traversal to " +goal_vertex+" is NOT UNCONSTRAINED.")
				return 0
			else:	
				print ("Traversal to " +goal_vertex+" is UNCONSTRAINED.")

	return 1


def checkUnconstrained(rdlt, goal_vertex, arc_list):
	#preprocessing
	vy_constraint = []
	xy_constraint = []
	checkIfTraversed = 1 #this variable keeps track if all the arcs have been traversed. essential for condition #3 of unconstrained arc
	for arc in rdlt.vertices[goal_vertex].getInArc():
		cons = arc.getConstraint()
		if (not(arc.checkIfTraversed())):
			checkIfTraversed = 0

		if(cons not in vy_constraint):
			vy_constraint.append(cons)

	for arc in arc_list:
		cons = rdlt.arcs[arc].getConstraint()
		if (cons not in xy_constraint):
			xy_constraint.append(cons)

	if ("EPSILON" not in xy_constraint):
			xy_constraint.append("EPSILON")

	# print (xy_constraint)
	# print (vy_constraint)
	# print (arc_list)
	#actualchecking
	for constraint in vy_constraint:
		if (constraint not in xy_constraint):
			#check for condition 3
			if(all(constraint == "EPSILON" for constraint in xy_constraint) and (checkIfTraversed == 0)):
				return 0
	return 1
	

def createRDLT():
	v, e = input().split()
	v = int(v)
	e = int(e)
	rdlt = RDLT()
	while(v!=0):
		v_id, v_type, v_rbs = input().split()
		rdlt.addVertex(v_id, v_type, v_rbs)
		v -= 1
	while(e!=0):
		e_id, e_cons, e_limit = input().split()
		arc = e_id.split("_")

		success = rdlt.addArc(e_id, arc[0], arc[1], e_cons, int(e_limit))
		if (success == 0):
			print ("Unsuccessful creation of arc")
			return 0
		e -= 1

	return rdlt

def getActivityProfile(start_vertex, final_vertex, vertices, arcs):
	total_config = input()
	total_config = int(total_config)
	activity_profile = []

	source_vertices = {}
	for i in vertices:
		source_vertices[i] = 0
	source_vertices[start_vertex] = 1
	
	for i in range(0, total_config):
		config = input().split()
		reach_config = []
		for conf in config:
			if (conf not in arcs):
				print ("Given arc is not in the arc set.")
				return 0
			con = conf.split("_")
			if (i == 0 and con[0] != start_vertex):
				print ("Invalid start vertex." + conf)
				return 0
			if (i == total_config and con[1] != final_vertex):
				print ("Invalid final vertex." + conf + str(i))
				return 0
			if ([con[0], con[1]] in reach_config):
				print ("Repeated arc " + conf + " at reachable configuration:"+ str(i))
				return 0

			if (source_vertices[con[0]] != 1):
				print("Not valid arc.")
				return 0

			source_vertices[con[1]] = 1
			reach_config.append([con[0], con[1]])

		activity_profile.append(reach_config)

	total_config -= 1
	return activity_profile

def checkSound(rdlt):
	for arc in rdlt.arcs.values():
		if (arc.checkIfTraversed() == 0):
			return 0
	return 1


#Creating the RDLT and activity profile
rdlt = createRDLT()
if (rdlt == 0):
	print("Unsuccessful creation of RDLT.")
	exit()

start_vertex, final_vertex = input().split()
if(not(start_vertex and final_vertex)):
	print ("Unsuccessful identification of start and final vertex")
	exit()

activity_profile = getActivityProfile(start_vertex, final_vertex, list(rdlt.vertices.keys()), list(rdlt.arcs.keys()))
if(activity_profile == 0):
	print ("Activity profile is NOT VALID.")
	exit()
else:
	print ("Activity profile is VALID.")

valid = validifyActivityProfile(rdlt, activity_profile, start_vertex, final_vertex)
if(valid == 1):
	print("Activity Profile is VERIFIED.")
else:
	print("Activity profile is NOT VERIFIED.")

sound = checkSound(rdlt)
if (sound):
	print ("RDLT is SOUND")
else:
	print ("RDLT is NOT SOUND")

#consider double entry of arcs and not existent vertices
