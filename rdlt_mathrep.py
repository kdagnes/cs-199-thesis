#This code is run using Python 3.6.2 and Numpy 1.14.0
#Added one time checking of L-constraint
#Added L-checking for whole configuration
import numpy as np

#Data Pre-processing
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

print("Input Configuration (Enter 0 when done):")

while(1):
	conf = input()
	if (conf == "0"):
		break
	conf = conf.split()
	X = np.zeros(len(vertices))
	Z = np.zeros(len(arcs))
	for pair in conf:
		for i in range(0, len(arcs)):
			if (pair == arcs[i]):
				Z[i] = 1
		pair = pair.split("_")
		for vertex in range(0, len(vertices)):
			if vertices[vertex] == pair[1]:
				X[vertex] = 1

	l_cons_new = l_cons + (matrix.dot(X))*Z
	print("L_k:" + str(l_cons_new)) 
	print("Arcs to be traversed:" + str(l_cons - l_cons_new) + "\n")	
	l_cons = l_cons_new

