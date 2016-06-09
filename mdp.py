#!/usr/bin/env python
# mdp implementation needs to go here
import rospy
from read_config import read_config
from copy import deepcopy
import numpy

#map
move_list = (read_config()["move_list"])
map_size = (read_config()["map_size"])
start = (read_config()["start"])
goal = (read_config()["goal"])
walls = (read_config()["walls"])
pits = (read_config()["pits"])
#probabilities
p_f = (read_config()["prob_move_forward"])
p_b = (read_config()["prob_move_backward"])
p_l = (read_config()["prob_move_left"])
p_r = (read_config()["prob_move_right"])
#rewards
r_step = (read_config()["reward_for_each_step"])
r_wall = (read_config()["reward_for_hitting_wall"])
r_goal = (read_config()["reward_for_reaching_goal"])
r_pit = (read_config()["reward_for_falling_in_pit"])
discount = (read_config()["discount_factor"])
#iteration
max_it = (read_config()["max_iterations"])
thresh_diff = (read_config()["threshold_difference"])

def m_opt_search():
	map_sizex = map_size[0]
	map_sizey = map_size[1]
	rewards = numpy.zeros((map_sizex+2,map_sizey+2))
	next_rewards = numpy.zeros((map_sizex+2,map_sizey+2))
	policy = []
	index = 0
	opt_move = [0,0]
	for i in range(0,map_sizex+2):
		for j in range(0,map_sizey+2):
			map_coord_x = i-1
			map_coord_y = j-1
			if ((i==0) or (j==0) or (i==(map_sizex+1)) or (j==(map_sizey+1))):
				rewards[i][j] = r_wall
			elif [map_coord_x , map_coord_y] in pits:
				rewards[i][j] = r_pit
			elif [map_coord_x , map_coord_y ] in walls:
				rewards[i][j] = r_wall
			elif ([map_coord_x , map_coord_y] == goal):
				rewards[i][j] = r_goal
			else:
				rewards[i][j] = 0
	rewards_diff = 1
	next_rewards = deepcopy(rewards)
	#print rewards
	while ((index < max_it) and (rewards_diff > thresh_diff)):
		policy = []	
		for i in range(1,map_sizex+1):
			for j in range(1,map_sizey+1):
				last_reward = -10
				current = [i,j]
				map_x = current[0]-1
				map_y = current[1]-1
				if [map_x,map_y] in pits:
					policy.append("PIT")
				elif [map_x,map_y] in walls:
					policy.append("WALL")
				elif ([map_x,map_y] == goal):
					policy.append("GOAL")
				else:
					for move in move_list:
						current = [i,j]
						for k in range(0,4):
							x = move_list[k][0] + i
							y = move_list[k][1] + j
							if (k == 0):
								if ((x==0) or 
									(y==0) or 
									(x==map_size[0]+1) or 
									(y==map_size[1]+1)):
									e_reward = discount*rewards[i][j] + r_wall
								elif ([x-1,y-1] in walls):
									e_reward = discount*rewards[i][j] + r_wall
								elif ([x-1,y-1] in pits):
									e_reward = r_pit + r_step
								elif ([x-1,y-1] == goal):
									e_reward = r_goal + r_step
								else:
									e_reward = discount*rewards[x][y] + r_step
							elif (k == 1):
								if ((x==0) or 
									(y==0) or 
									(x==map_size[0]+1) or 
									(y==map_size[1]+1)):
									w_reward = discount*rewards[i][j] + r_wall
								elif ([x-1,y-1] in walls):
									w_reward = discount*rewards[i][j] + r_wall
								elif ([x-1,y-1] in pits):
									w_reward = r_pit + r_step
								elif ([x-1,y-1] == goal):
									w_reward = r_goal + r_step
								else:
									w_reward = discount*rewards[x][y] + r_step
							elif (k == 2):
								if ((x==0) or 
									(y==0) or 
									(x==map_size[0]+1) or 
									(y==map_size[1]+1)):
									s_reward = discount*rewards[i][j] + r_wall
								elif ([x-1,y-1] in walls):
									s_reward = discount*rewards[i][j] + r_wall
								elif ([x-1,y-1] in pits):
									s_reward = r_pit + r_step
								elif ([x-1,y-1] == goal):
									s_reward = r_goal + r_step
								else:
									s_reward = discount*rewards[x][y] + r_step
							elif (k == 3):
								if ((x==0) or 
									(y==0) or 
									(x==map_size[0]+1) or 
									(y==map_size[1]+1)):
									n_reward = discount*rewards[i][j] + r_wall + r_step
								elif ([x-1,y-1] in walls):
									n_reward = discount*rewards[i][j] + r_wall + r_step
								elif ([x-1,y-1] in pits):
									n_reward = r_pit + r_step
								elif ([x-1,y-1] == goal):
									n_reward = r_goal + r_step
								else:
									n_reward = discount*rewards[x][y] + r_step
						if (move == [0,1]):
							f_reward = e_reward
							b_reward = w_reward
							r_reward = s_reward
							l_reward = n_reward
						elif (move == [0,-1]):
							f_reward = w_reward
							b_reward = e_reward
							r_reward = n_reward
							l_reward = s_reward
						elif (move == [1,0]):
							f_reward = s_reward
							b_reward = n_reward
							r_reward = w_reward
							l_reward = e_reward
						else:
							f_reward = n_reward
							b_reward = s_reward
							r_reward = e_reward
							l_reward = w_reward
						reward = (p_f*f_reward + p_b*b_reward + p_r*r_reward + p_l*l_reward)
						if (reward >= last_reward):
							opt_move[0] = current[0] + move[0]
							opt_move[1] = current[1] + move[1]
							#if ((opt_move[0]==0) 
							#	or (opt_move[1]==0) 
							#	or (opt_move[0]==map_size[0]+1) 
							#	or (opt_move[1]==map_size[1]+1)):
							#	next_move = "WALL"
							#elif [(opt_move[0]-1),(opt_move[1]-1)] in pits:
							#	next_move ="PIT"
							#elif [(opt_move[0]-1),(opt_move[1]-1)] in walls:
							#	next_move = "WALL"
							#elif ([(opt_move[0]-1),(opt_move[1]-1)] == goal):
							#	next_move = "GOAL"
							if move == [0,1]:
								next_move = "E"
							elif move == [0,-1]:
								next_move = "W"
							elif move == [1,0]:
								next_move = "S"
							else:
								next_move = "N"	
							next_rewards[i][j] = reward
							last_reward = reward
					policy.append(next_move)
		index +=1
		oldsum = numpy.sum(rewards)
		newsum = numpy.sum(next_rewards)
		rewards_diff = abs(oldsum-newsum)
		rewards = deepcopy(next_rewards)
		#print next_rewards
	print
	print "MDP Results"
	print "Optimal Policy:"
	print policy
	return policy
#def calculate_opt_policy(self, message):
	

