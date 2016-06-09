#!/usr/bin/env/ python

import rospy
import json
from read_config import read_config
from copy import deepcopy
import numpy
import random

move_list = (read_config()["move_list"])
map_size = (read_config()["map_size"])
iterations = (read_config()["p_iterations"])

def p_learn():
	map_sizex = map_size[0]
	map_sizey = map_size[1]
	rewards = numpy.zeros((map_sizex+2,map_sizey+2))
	transitions = numpy.zeros(5)
	indexes = numpy.zeros(4)
	reward = 0
	count = 0
	move = []
	dest = []
	print "gets here"
	for n in range(0,iterations):
		for i in range(0,map_sizex):
			for j in range(0,map_sizey):
				for d in range(0,4):
					count += 1
					move = move_list[d]
					[dest, val, reward] = p_move([i,j],move)
					rewards[dest[0]+1][dest[1]+1] = reward
					indexes[val] += 1
					if [i,j] == dest:
						transitions[0] += 1
					elif [i+move[0],j+move[1]] == dest:
						transitions[3] += 1
					elif [i-move[0],j-move[1]] == dest:
						transitions[2] += 1
					elif (d == 0):
						if ([i-1, j] == dest):
							transitions[1] += 1
						else:
							transitions[4] += 1
						#elif [i, j-1] == dest:
						#	transitions[2] += 1
					elif (d == 1):
						if ([i+1, j] == dest):
							transitions[1] += 1
						else:
							transitions[4] += 1
						#elif [i, j+1] == dest:
						#	transitions[2] += 1
					elif (d == 2):
						if ([i, j-1] == dest):
							transitions[1] += 1
						else:
							transitions[4] += 1
						#elif [i-1, j] == dest:
						#	transitions[2] += 1
					else:
						if ([i, j+1] == dest):
							transitions[1] += 1
						else:
							transitions[4] += 1
						#elif [i+1, j] == dest:
						#	transitions[2] += 1
	print indexes
	print transitions/count
	print rewards

#probabilities
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

def p_move(start,direction):
	probs = [p_f,p_b,p_l,p_r]
	map_sizex = map_size[0]
	map_sizey = map_size[1]
	r = random.random()
	index = 0
	move = []
	trans = numpy.zeros(4)
	while(r>=0 and index < len(probs)):
		r -= probs[index]
		index += 1
	index = index-1
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
	elif (move in pits):
		reward = r_p
	elif (move == goal):
		reward = r_g
	else:
		reward = r_s
	#trans[index] += 1
	#print trans
	return [move, index, reward]
