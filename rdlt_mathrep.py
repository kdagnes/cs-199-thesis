#This code is run using Python 3.6.2 and Numpy 1.14.0

import numpy as np

class RDLT:

	def __init__(self, vertices, l_cons, c_cons):
		self.vertices = []
		self.l_cons = []
		self.c_cons = []
		self.matrix =[]
		self.arcs = []

#Getting the data
vertices = np.array(input("Vertices:").split())
arcs = np.array(input("Arcs:").split())
l_cons=np.array(input("L Constraint:").split())
l_cons=[int(i) for i in l_cons]
c_cons=np.array(input("C Constraint:").split())

print("Matrix:")
matrix = np.zeros(shape=(len(vertices), len(arcs)))
for i in range(0, len(arcs)):
 	j = input().split()
 	j = [int(k) for k in j]
 	matrix[i] = j



