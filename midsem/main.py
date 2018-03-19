from matrix import *
#from graph import *
import numpy as np
from sympy import Abs, Symbol
import sys

def matrixMethod(output_file,vertices, arcs, phi_zero, omega_zero, activity_profile):

	verify, rho = verifyActivityProfile(vertices, arcs, omega_zero, phi_zero, activity_profile)
	if(verify == 1):
		output_file.write("Activity Profile is VALID\n")
	else:
		output_file.write("Activity Profile is NOT VALID\n")
		output_file.write("Activity Profile is NOT SOUND\n")
		output_file.write(verify)
		return
		
		
	if(all(rho_id >= 1 for rho_id in rho)):
		output_file.write("RDLT is SOUND\n")
	else:
		output_file.write("RDLT is NOT SOUND\n")
		output_file.write("Not all arcs were traversed.\n")

	return

# def graphMethod(output_file,vertices, vertex_types, arcs, phi, omega, activity_profile):
# 	rdlt = createRDLT(vertices, vertex_types, arcs, phi, omega)
# 	if (rdlt == 0):
# 		output_file.write("Unsuccessful creation of RDLT.\n")
# 		exit()

# 	valid = validifyActivityProfile(rdlt, activity_profile)
# 	if(valid == 1):
# 		output_file.write("Activity Profile is VALID.\n")
# 	else:
# 		output_file.write("Activity profile is NOT VALID.\n")

# 	sound = checkSound(rdlt)
# 	if (sound):
# 		output_file.write ("RDLT is SOUND\n")
# 	else:
# 		output_file.write ("RDLT is NOT SOUND\n")
# 		output_file.write ("Not all arcs were traversed.\n")
	
# 	return

def getActivityProfile(ap_file, start_vertex, final_vertex, vertices, arcs, total_config):
	activity_profile = []

	source_vertices = {}
	for i in vertices:
		source_vertices[i] = 0
	source_vertices[start_vertex] = 1
	
	for i in range(0, total_config):
		config = ap_file.readline().split()
		reach_config = []
		error = ""
		for conf in config:
			if (conf not in arcs):
				error = "RC:"+str(i+1)+" " +conf +" is not in the arc set."
				return ([], error)
			con = conf.split("_")
			if (i == 0 and con[0] != start_vertex):
				error = "RC:"+str(i+1)+" " +conf+ "is an invalid start vertex."
				return ([], error)
			if (i == total_config and con[1] != final_vertex):
				error ="RC:"+str(i+1)+ " " + conf+ " is an invalid final vertex." 
				return ([], error)
			if ([con[0], con[1]] in reach_config):
				error = "RC:"+str(i+1)+" " + conf+" is duplicated."
				return ([], error)

			if (source_vertices[con[0]] != 1):
				error = "RC:"+str(i+1)+" " + conf+" is not valid arc because "+ con[0]+" is not yet traversed/explored."
				return ([], error)

			source_vertices[con[1]] = 1
			reach_config.append([con[0], con[1]])

		activity_profile.append(reach_config)

	total_config -= 1
	return (activity_profile, "No error")

rdlt_file = open(sys.argv[1], 'r')
ap_file = open(sys.argv[2], 'r')

matrix_file = open('matrix_'+sys.argv[2], 'w')
# graph_file = open('graph_'+sys.argv[2], 'w')

vertices = rdlt_file.readline().split()
vertex_types = rdlt_file.readline().split()
arcs = rdlt_file.readline().split()
phi = rdlt_file.readline().split()
phi=np.array([int(i) for i in phi])
omega = rdlt_file.readline().split()
omega =np.array([Symbol(i, positive=True) for i in omega])

#(1) & (2)  Check whether the given activity profile is correct
start_vertex, final_vertex = ap_file.readline().split()
if(not(start_vertex and final_vertex)):
	matrix_file.write("No start and/or final vertices given.\n")
	# graph_file.write("No start and/or final vertices given.\n")
	exit()

total_config = ap_file.readline()
total_config = int(total_config)
activity_profile, error = getActivityProfile(ap_file, start_vertex, final_vertex, vertices, arcs, total_config)
if (activity_profile != []):
	matrix_file.write("Activity Profile is CORRECT\n") 
	# graph_file.write("Activity Profile is CORRECT\n") 
else:
	message = "Activity Profile is NOT CORRECT\nActivity Profile is NOT VALID\nActivity Profile is NOT SOUND\n" + error
	matrix_file.write(message) 
	# graph_file.write(message)
	
matrixMethod(matrix_file, vertices, arcs, phi, omega, activity_profile)
# graphMethod(graph_file,vertices, vertex_types, arcs, phi, omega, activity_profile)

matrix_file.close()
# graph_file.close()