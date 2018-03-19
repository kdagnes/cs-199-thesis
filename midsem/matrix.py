import numpy as np
from sympy import Abs, Symbol

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

		unconstrained = checkIfUnconstrained(omega, phi, rho, alpha, beta, phi_zero, omega_zero, omega_zero_alpha, arcs)

		if(unconstrained != 1):
			error = "RC:"+str(rc_id+1)+" "+unconstrained
			return (error, []) 
		OMEGA.append(omega)
		PHI.append(phi)

	return (1, rho)

def checkIfUnconstrained(omega, phi, rho, alpha, beta, phi_zero, omega_zero, omega_zero_alpha, arcs):
	if(not(all(ab >= 0 for ab in phi))):
		error = "Condition 1:Limit traversal is reached"
		return error

	# for arc_id, ab in enumerate(omega):
	# 	if(ab not in omega_zero_alpha)):
	# 		print("Consition not 2.a satisfied")
	# 		return 0

	if(all ((ab in omega_zero_alpha) for ab in omega)):
#		print("Consition 2.a satisfied")
		return 1

	for omega_id in range(0, len(omega)):
			#get the x,y of the v,y
			for alpha_id in range(0, len(alpha)):
				if ((alpha[alpha_id] == 1) and (arcs[alpha_id].split("_")[1] == arcs[omega_id].split("_")[1])):
					if (omega[omega_id] not in omega_zero_alpha):
						if (not(rho[omega_id] >= 1)):
							error = "Arc " + arcs[omega_id] + " is preventing traversal of arc " + arcs[alpha_id]
							return error

						if (omega_zero[alpha_id] != Symbol("EPSILON", positive=True)):
							print ( str(omega_zero[alpha_id])  +"!=EPSILON")
							error = "Arc " + arcs[omega_id] + " is preventing traversal of arc " + arcs[alpha_id]
							return error

	return 1
	# else:

		# for arc_id, ab in enumerate(omega):
		# 	result = arcs[arc_id].split("_")[1]
		# 	if (omega[arc_id] == "EPSILON"):
		# 		for rho_id, arc_num in enumerate(arcs):
		# 			if (not(arc_num == arcs[arc_id].split("_")[1] and rho[rho_id] >= 1)):
		# 				error = arcs[arc_id] + " is not an unconstrained arc."
		# 				print ("Condition 2 is not satisfied")
		# 				return error
		# 	elif(omega[arc_id] != "EPSILON"):
		# 		print (omega[arc_id])
		# 		error = arcs[arc_id] + " is not an unconstrained arc."
		# 		print ("Consition 2.b is not satisfied")
		# 		return error
		# 	else:
		# 		#print("Condition 2.b is satisfied")
		# 		return 1
