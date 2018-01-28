class Vertex:
    def __init__(self, node, type):
        self.id = node
        self.type = type #'b' - boundary,'e' - entity,'c' - controller

    def __str__(self):
        return str(self.id)
class Arc:
	def __init__(self, edge, fromNode, toNode):
		self.id = edge
		self.fromNode = fromNode
		self.toNode = toNode
	
class RDLT:
	def __init__(self):
		self.vertices = {}
		self.arcs = []
		self.num_vertices = 0
		self.num_arcs = 0
		
	def addVertex(self, node, type):
		self.vertices[node] = Vertex(node,type)
	
	def getVertex(self, node):
		return self.vertices[node]
	
	def addArc(self, edge, fromNode, toNode):
		self.arcs.append(Edge(edge, fromNode, toNode))

		
rdlt = RDLT()
rdlt.addVertex('v_a','b')
print (rdlt.vertices['v_a'].type)