#This code is run using Python 3.6.2 and Numpy 1.14.0
#Added one time checking of L-constraint
#Added L-checking for whole configuration
import numpy as np
import pandas as pd
from sympy import *

def checkValidActivityProfile(activity_profile, vertices, start_vertex, final_vertex):
	source_vertices = {}
	for i in vertices:
		source_vertices[i] = 0

	for arc in activity_profile[0]:
		if(arc[0] == start_vertex):
			source_vertices[arc[0]] = 1
		else:
			return 0;	

	for idx, reach_config in enumerate(activity_profile):
		for arc in reach_config:
		 	if (source_vertices[arc[0]] == 1):
		 		source_vertices[arc[1]] = 1
		 	else:
		 		return 0;

	for arc in activity_profile[-1]:
		if (arc[1] != final_vertex):
			return 0;

	return 1;


def checkLCY (L, C, Y):


#Creating the static representation of RDLT
vertices = np.array(input("Vertices:").split())
arcs = np.array(input("Arcs:").split())
l_cons=input("L Constraint:").split()
l_cons=np.array([int(i) for i in l_cons])
c_cons=input("C Constraint:").split()
c_cons=np.array([Symbol(i) for i in c_cons])

print("Matrix:")
matrix = pd.DataFrame(np.zeros(shape=(len(vertices), len(arcs))), columns=vertices)
matrix = matrix.set_index(arcs)

for arc in arcs:
	dest_vertex = arc.split("_")
	dest_vertex = dest_vertex[1]
	matrix.set_value(arc, dest_vertex, -1)
#print (matrix)


#Activity Profile
print("Input Reachability Configuration per timestep (Enter 0 when done):")
activity_profile = []
while(1):
	reach_config = input()
	if (reach_config == "0" or reach_config == ""):
		break
	reach_config = reach_config.split()
	rc = []
	for arc in reach_config:
		arc = arc.split("_")
		rc.append(arc)

	activity_profile.append(rc)

#print(activity_profile)

start_vertex = input("Start vertex:")
final_vertex = input("Final vertex:")

if (0 == checkValidActivityProfile(activity_profile, vertices, start_vertex, final_vertex)):
	exit("\nInvalid Activity Profile due to inconsistency in the given arcs.\n")

L = l_cons
C = c_cons
X = {}
Z = {}
for reach_config in activity_profile:
	for i in vertices:
		X[i] = 0
	for j in arcs:
		Z[j] = 0

	for arc in reach_config:
		X[arc[1]] = 1
		Z[arc[0]+'_'+arc[1]] = 1

	Y = matrix.dot([v for v in X.values()])

	L = L + Y*[v for v in Z.values()]
	C = C - c_cons*[v for v in Z.values()]
	print(L)
	print(C)

	checkLCY(L, C, Y)