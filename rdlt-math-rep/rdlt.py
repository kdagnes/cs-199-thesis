import numpy as np
from sympy import Abs, Symbol

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
				print ("Reachability Configuration:"+str(i+1)+"Given arc is not in the arc set: "+  conf)
				return 0
			con = conf.split("_")
			if (i == 0 and con[0] != start_vertex):
				print ("Reachability Configuration:"+str(i+1)+"Invalid start vertex." + conf)
				return 0
			if (i == total_config and con[1] != final_vertex):
				print ("Reachability Configuration:"+str(i+1)+"Invalid final vertex." + conf + str(i))
				return 0
			if ([con[0], con[1]] in reach_config):
				print ("Reachability Configuration:"+str(i+1)+"Repeated arc " + conf + " at reachable configuration:"+ str(i))
				return 0

			if (source_vertices[con[0]] != 1):
				print("Reachability Configuration:"+str(i+1)+"Not valid arc.")
				return 0

			source_vertices[con[1]] = 1
			reach_config.append([con[0], con[1]])

		activity_profile.append(reach_config)

	total_config -= 1
	return activity_profile

def verifyActivityProfile(vertices, arcs, omega_zero, phi_zero, activity_profile):
	omega = omega_zero[:]
	phi = phi_zero[:]

	arc_length = len(arcs)
	OMEGA = []
	PHI = []
	count = 0
	for rc_id, reach_config in enumerate(activity_profile):
		alpha = [0]*arc_length
		beta = [0]*arc_length
		rho = [0]*arc_length
		for arc_id, arc in enumerate(arcs):
			for xy_arc in reach_config:
				if(arc == xy_arc[0]+"_"+xy_arc[1]):
					alpha[arc_id] = 1
				if(arc.split("_")[1] == xy_arc[1]):
					beta[arc_id] = 1


		omega = omega_zero*beta - omega_zero*alpha
		omega = np.absolute(omega)

		omega_zero_alpha = set([0,Symbol("EPSILON", positive=True)])
		for ab in omega_zero*alpha:
			omega_zero_alpha.add(ab)

		phi = phi - alpha
		rho = phi_zero - phi

		# print(alpha)
		# print (beta)
		# print (omega_zero_alpha)
		# print (omega)
		# print (phi)
		# print (rho)


		unconstrained = checkIfUnconstrained(omega, phi, rho, alpha, beta, phi_zero, omega_zero, omega_zero_alpha, arcs)

		if(unconstrained == 0):
			print("Reachability Configuration:"+rc_id)
			return 0
		OMEGA.append(omega)
		PHI.append(phi)

	return 1, rho


def checkIfUnconstrained(omega, phi, rho, alpha, beta, phi_zero, omega_zero, omega_zero_alpha, arcs):
	if(not(all(ab >= 0 for ab in phi))):
		print("Condition 1:Limit traversal is reached")
		return 0

	# for arc_id, ab in enumerate(omega):
	# 	if(ab not in omega_zero_alpha)):
	# 		print("Consition not 2.a satisfied")
	# 		return 0

	if(all ((ab in omega_zero_alpha) for ab in omega)):
		#print("Consition 2.a satisfied")
		return 1
	else:
		for arc_id, ab in enumerate(omega):
			result = arcs[arc_id].split("_")[1]
			if (result[arc_id] == "EPSILON"):
				for rho_id, arc_num in enumerate(arcs):
					if (not(arc_num == arcs[arc_id].split("_")[1] and rho[rho_id] >= 1)):
						print ("Condition 2 is not satisfied")
						return 0
			else:
				#print("Consition 2.b satisfied")
				return 1


vertices = input().split()
arcs = input().split()
phi_zero = input().split()
phi_zero=np.array([int(i) for i in phi_zero])
omega_zero = input().split()
omega_zero=np.array([Symbol(i, positive=True) for i in omega_zero])

#(1) & (2)  Check whether the given activity profile is correct
start_vertex, final_vertex = input().split()
activity_profile = getActivityProfile(start_vertex, final_vertex, vertices, arcs)
if (activity_profile == 0):
	print ("Activity Profile is NOT VALID")
	exit()
else:
	print ("Activity Profile is VALID") 

verify, sound = verifyActivityProfile(vertices, arcs, omega_zero, phi_zero, activity_profile)
if(verify == 1):
	print ("Activity Profile is VERIFIED")
else:
	print ("Activity Profile is NOT VERIFIED")

if(all(rho_id >= 1 for rho_id in sound)):
	print ("RDLT is SOUND")
else:
	print ("RDLT is NOT SOUND")
