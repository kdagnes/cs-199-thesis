#This code is run using Python 3.6.2 and Numpy 1.14.0
#Added one time checking of L-constraint
#Added L-checking for whole configuration
#Removed destination matrix

import numpy as np
from sympy import *

def checkValidActivityProfile(activity_profile, vertices, start_vertex, final_vertex):
	source_vertices = {}
	for i in vertices:
		source_vertices[i] = 0

	for idx, reach_config in enumerate(activity_profile):
		for arc in reach_config:
			if((arc[0] not in vertices) or (arc[1] not in vertices)):
				print("\nArc "+str(arc[0]) + "_" + str(arc[1]) + " is not valid because " + str(arc[0]) + " or " + str(arc[1]) + " is not in the vertex set." )
				return 0
			if(reach_config.count(arc) != 1):
				print ("\nRepeated arc " +str(arc[0]) + "_" + str(arc[1]) + " at timestep " + str(idx))
				return 0

	for arc in activity_profile[0]:
		if(arc[0] == start_vertex):
			source_vertices[arc[0]] = 1
		else:
			print("\nNot start vertex")
			return 0

	for idx, reach_config in enumerate(activity_profile):
		for arc in reach_config:
		 	if (source_vertices[arc[0]] == 1):
		 		source_vertices[arc[1]] = 1
		 	else:
		 		print("\nNot corresponding")
		 		return 0

	for arc in activity_profile[-1]:
		if (arc[1] != final_vertex):
			print("\nNot final vertex")
			return 0

	return 1;


def checkLCY (L, C, Y, C_init):	
	
	LC = [0,0]	
	if (any(arc < 0 for arc in L)):
		print ("L not satisfied")
		LC[0] = 1

	HQ = []
	for id_y, y in enumerate(Y):
		if ((y == -1) and (C[id_y] == 0) and (C_init[id_y] not in HQ)):
			HQ.append(C_init[id_y])
	for i in range(0, len(Y)):
		if(Y[i] == -1 and (C[i] not in [0, Symbol("eps"), HQ])): #No HQ yet
			print("C constraint is not satisfied: " + str(C[i]))
			LC[1] = 1
	return LC



def Generate(S, V, E, start_vertex, final_vertex):
	C = E['C']
	L = E['L']
	arcs = E['ID']

	activity_profile = S
	P = V
	if (0 == checkValidActivityProfile(activity_profile, P, start_vertex, final_vertex)):
		exit("Invalid Activity Profile.\nThe given activity profile is not verified \nThe given activity profile is not sound")
		# print("Invalid Activity Profile.\nThe given activity profile is not verified \nThe given activity profile is not sound")
		# return 0, 0
	else:
		print("The given activity profile is valid")

	C_init = C
	X = {}
	Z = {}
	Y = {}
	L_vector = []
	C_vector = []

	L_vector.append(np.array(L))
	C_vector.append(np.array(C))

	for idy, reach_config in enumerate(S):
		print("\nTimestep: "+str(idy))
		print(L)
		print(C)
		for i in V:
			X[i] = 0
		for j in arcs:
			Z[j] = 0
			Y[j] = 0


		list_of_goal_vertices = []
		for idx, arc in enumerate(reach_config):
			X[arc[1]] = 1
			Z[arc[0]+'_'+arc[1]] = 1

			if(arc[1] not in list_of_goal_vertices):
				for y in arcs:
					lala = y.split("_")
					if(arc[1] == lala[1]):
						Y[lala[0]+'_'+lala[1]] = -1
				list_of_goal_vertices.append(arc[1])


		Y_new = np.array([y for y in Y.values()])
		Z_new = np.array([v for v in Z.values()])
		#Y = matrix.dot([v for v in X.values()])

		L = L + Y_new*Z_new
		
		for id_c, c_elem in enumerate(C):
			if (c_elem != 0):
				C[id_c] = C[id_c] - C_init[id_c]*Z_new[id_c]

		#print (Z_new)

		check = checkLCY(L, C, Y_new, C_vector[0])
		if (any(constraint == 1 for constraint in check)):
			Err = (idx, check)
			S = {'L':L_vector, 'C':C_vector}
			return S, Err
		L_vector.append(np.array(L))
		C_vector.append(np.array(C))


	print("\nTimestep: "+str(idy+1))
	print(L)
	print(C)
	S =  {'L':L_vector, 'C':C_vector}
	return S, 0

def Verify(S, V, E, start_vertex, final_vertex):
	S_vector, Err = Generate(S, V, E, start_vertex, final_vertex)
	if (Err != 0):
		print("Error in Generating S'")
		return 0

	L = S_vector['L']
	C = S_vector['C']
	arcs = E['ID']

	for id_rc, reach_config in enumerate(S):
		L_result = L[id_rc] - L[id_rc+1]
		for id_r, r in enumerate(L_result):
			if (r == 0 and (arcs[id_r].split("_") in reach_config)):
				print("Error_Verify: First If in For Loop")
				return 0
			if (r == 1 and (arcs[id_r].split("_") not in reach_config)):
				print("Error_Verify: Second If in For Loop")
				return 0

		for id_c, c in enumerate(C[id_rc+1]):
			if(c != 0 and (arcs[id_c].split("_") in reach_config)):
				print(str(id_rc) + "Fuck" + str(id_c))
				print("Error_Verify: Third If in For Loop")
				return 0

	return S_vector


def Sound(S, V, E, start_vertex, final_vertex):
	S_vector = Verify(S, V, E, start_vertex, final_vertex)

	if (S_vector == 0):
		print("The given activity profile is not verified.")
		return 0
	else:
		print ("The given activity profile is verified")
		C = S_vector['C']
		if (any(c != 0 for c in C[len(C)-1])):
			print("Not sound because not all arcs are traversed at least once")
			print(C[len(C)-1])
			return 0
		return 1

#Input RDLT

#Creating the static representation of RDLT
vertices = np.array(input("Vertices:").split())
arcs= np.array(input("Arcs:").split())
l_cons=input("L Constraint:").split()
l_cons=np.array([int(i) for i in l_cons])
c_cons=input("C Constraint:").split()
c_cons=np.array([Symbol(i) for i in c_cons])


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

print("\n\nResult:")
E = {'ID':arcs, 'L':l_cons, 'C':c_cons}

if(Sound(activity_profile, vertices, E, start_vertex, final_vertex)):
	print ("The given RDLT is sound")