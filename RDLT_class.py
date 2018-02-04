class Vertex:
    def __init__(self, node, type):
        self.id = node
        self.type = type #'b' - boundary,'e' - entity,'c' - controller

    def __str__(self):
        return "ID:" + str(self.id) + " Type:" + str(self.type) 
		
class Arc:
	def __init__(self, edge, fromNode, toNode, constraint, limit):
		self.id = edge	#string
		self.fromNode = fromNode #string
		self.toNode = toNode #string
		self.constraint = constraint #string
		self.limit = limit #integer
		
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

class RDLT:
	def __init__(self):
		self.vertices = {} #dictionary
		self.arcs = {}	#dictionary
		self.num_vertices = 0
		self.num_arcs = 0
		
	def addVertex(self, node, type):
		self.vertices[node] = Vertex(node,type)
		self.num_vertices += 1
	
	#return Vertex object
	def getVertex(self, node):
		return self.vertices[node]
	
	def addArc(self, edge, fromNode, toNode, constraint, limit):
		self.arcs[edge] = Arc(edge, fromNode, toNode, constraint, limit)
		self.num_arcs += 1
	
	#return Arc object
	def getArc(self, edge):
		return self.arcs[edge]

		
rdlt = RDLT()
rdlt.addVertex('u_1','b')
rdlt.addVertex('u_2','c')
rdlt.addVertex('u_3','c')
rdlt.addVertex('u_4','b')

rdlt.addArc('1', 'u_1', 'u_2', 'epsilon',1)
rdlt.addArc('2', 'u_1', 'u_3', 'epsilon',1)
rdlt.addArc('3', 'u_2', 'u_4', 'a',1)
rdlt.addArc('4', 'u_3', 'u_4', 'b',1)
