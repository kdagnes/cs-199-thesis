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
		if(not(self.vertices[fromNode] and self.vertices[toNode])):
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
		print ("Reachability Configuration: " + str(id_config))
		y_vertices = []

		#check if L-constraint is satisfied
		#and get the goal vertices
		for arc in config:
			arc_id = arc[0] + "_" + arc[1]
			print(rdlt.arcs[arc_id].getLimit())
			if(rdlt.arcs[arc_id].getLimit() <= 0):
				print ("Limit traversal is reached")
				return 0
			else:
				rdlt.arcs[arc_id].lessenLimit()

			if(arc[1] not in y_vertices):
				y_vertices.append(arc[1])

		for goal_vertex in y_vertices:
			arc_list = []
			for arc in config:
				if (arc[1] == goal_vertex):
					arc_list.append(arc[0]+"_"+arc[1])
				
			print (goal_vertex)
			if (checkUnconstrained(rdlt, goal_vertex, arc_list) == 0):
				print ("Not unconstrained.")
				return 0
			else:
				print ("Unconstrained")
			
	return 1


def checkUnconstrained(rdlt, goal_vertex, arc_list):
	#preprocessing
	vy_constraint = []
	xy_constraint = []
	for arc in rdlt.vertices[goal_vertex].getInArc():
		cons = arc.getConstraint()
		if(cons not in vy_constraint):
			vy_constraint.append(cons)

	for arc in arc_list:
		cons = rdlt.arcs[arc].getConstraint()
		if (cons not in xy_constraint):
			xy_constraint.append(cons)

	if ("EPSILON" not in xy_constraint):
			xy_constraint.append("EPSILON")

	print (xy_constraint)
	print (vy_constraint)
	#actualchecking
	for constraint in vy_constraint:
		if (constraint not in xy_constraint):
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
		rdlt.addArc(e_id, arc[0], arc[1], e_cons, int(e_limit))
		e -= 1

	return rdlt

def getActivityProfile():
	total_config = input()
	total_config = int(total_config)
	activity_profile = []
	while(total_config != 0):
		config = input().split()
		reach_config = []
		for conf in config:
			con = conf.split("_")
			if (con in reach_config):
				print("Repeated arc: " + conf )
				return 0
			reach_config.append([con[0], con[1]])
		activity_profile.append(reach_config)

		total_config -= 1
	return activity_profile

#Creating the RDLT and activity profile
rdlt = createRDLT()
if (rdlt == 0):
	print("Unsuccessful creation of RDLT.")
	exit()

activity_profile = getActivityProfile()
if(activity_profile == 0):
	print ("Unsuccessful creation of activity profile.")
	exit()
start_vertex, final_vertex = input().split()
if(not(start_vertex and final_vertex)):
	print ("Unsuccessful identification of start and final vertex")
	exit()
valid = validifyActivityProfile(rdlt, activity_profile, start_vertex, final_vertex)
if(valid == 1):
	print("Activity Profile is VALID.")
	exit()
else:
	print("Activity profile is NOT VALID.")

#consider double entry of arcs and not existent vertices
