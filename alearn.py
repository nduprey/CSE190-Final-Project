#!/usr/bin/env/ python

import rospy
import json
from read_config import read_config
from copy import deepcopy
import numpy
import random

move_list = (read_config()["move_list"])
map_size = (read_config()["map_size"])
iterations = (read_config()["a_iterations"])
p_f = (read_config()["prob_move_forward"])
p_b = (read_config()["prob_move_backward"])
p_l = (read_config()["prob_move_left"])
p_r = (read_config()["prob_move_right"])
r_s = (read_config()["reward_for_each_step"])
r_w = (read_config()["reward_for_hitting_wall"])
r_g = (read_config()["reward_for_reaching_goal"])
r_p = (read_config()["reward_for_falling_in_pit"])
walls = (read_config()["walls"])
pits = (read_config()["pits"])
goal = (read_config()["goal"])	
start = (read_config()["start"])
gamma = (read_config()["gamma"])
alpha = (read_config()["discount_factor"])
	
def a_learn():
	map_sizex = map_size[0]
	map_sizey = map_size[1]
	q_vals = numpy.zeros((map_sizex,map_sizey,4))
	policy = []
	direc = []
	direc.append('E')
	direc.append('W')
	direc.append('S')
	direc.append('N')
	index = 0
	#for n in range(0,iterations):
	#	for i in range(0,map_sizex):
	#		for j in range(0,map_sizey):
	#			for d in range(0,4):
	for i in range(0,iterations):
		loc = start
		policy = []
		while not ((loc in pits) or (loc == goal)):
			#print loc
			index += 1
			r = random.randint(0,3)
			[dest, reward] = p_move(loc, move_list[r])
			last_q = q_vals[loc[0]][loc[1]][r]
			next_q = reward + gamma*numpy.amax(q_vals[dest[0]][dest[1]])
			#q_vals[loc[0]][loc[1]][r] = (1-gamma)*last_q + gamma*next_q
			q_vals[loc[0]][loc[1]][r] = last_q + alpha*(next_q - last_q)
			loc = dest
		for i in range(0,map_sizex):
			for j in range(0,map_sizey):
				max_val = numpy.argmax(q_vals[i][j])
				#print max_val
				if ([i,j] == goal):
					policy.append('GOAL')
				elif ([i,j] in pits):
					policy.append('PIT')
				elif ([i,j] in walls):
					policy.append('WALL')
				elif (max_val == 0):
					policy.append('E')
				elif (max_val == 1):
					policy.append('W')
				elif (max_val == 2):
					policy.append('S')
				else:
					policy.append('N')
	print
	print "Active Learning Results"
	print "Optimal Policy:"
	print policy
	print "Q-Values:"
	print q_vals
	print "[EAST , WEST , SOUTH, NORTH]"

def p_move(start,direction):
	probs = [p_f,p_b,p_l,p_r]
	map_sizex = map_size[0]
	map_sizey = map_size[1]
	r = random.random()
	index = 0
	move = []
	trans = numpy.zeros(4)
	#while(r>=0 and index < len(probs)):
	#	r -= probs[index]
	#	index += 1
	#index = index-1
	if (index == 0):
		move = [start[0] + direction[0], start[1] + direction[1]]
	elif (index == 1):
		move = [start[0] - direction[0], start[1] - direction[1]]
	elif (index == 2):
		if direction == [0,1]:
			move = [start[0] - 1, start[1]]
		elif direction == [0,-1]:
			move = [start[0] + 1, start[1]]
		elif direction == [1,0]:
			move = [start[0], start[1] + 1]
		elif direction == [-1,0]:
			move = [start[0], start[1] - 1]
	elif (index == 3):
		if direction == [0,1]:
			move = [start[0] + 1, start[1]]
		elif direction == [0,-1]:
			move = [start[0] - 1, start[1]]
		elif direction == [1,0]:
			move = [start[0], start[1] - 1]
		elif direction == [-1,0]:
			move = [start[0], start[1] + 1]
	if ((move in walls) or (move[0] < 0) or (move[0] >= map_sizex) or (move [1] < 0) or (move[1] >= map_sizey)):
		reward = r_w
		move = start
	elif (move in pits):
		reward = r_p + r_s
	elif (move == goal):
		reward = r_g + r_s
	else:
		reward = r_s
	#trans[index] += 1
	#print trans
	return [move, reward]
