#!/usr/bin/env/ python
# astar implementation needs to go here
import rospy
import json
from read_config import read_config
from copy import deepcopy

move_list = (read_config()["move_list"])
map_size = (read_config()["map_size"])
start = (read_config()["start"])
goal = (read_config()["goal"])
walls = (read_config()["walls"])
pits = (read_config()["pits"])


def a_opt_search():
	current = start
	#print "startx:",current[0]
	#print "starty:",current[1]
	opt_list = []
	next_move = [0,0]
	opt_list.append(deepcopy(current))
	index = 0
	while (current != goal) and (index < 50):
		last_dist = map_size[0]+map_size[1]
		for move in move_list:
			dist = abs(current[0] + move[0] - goal[0]) + abs(current[1] + move[1] - goal[1])
			legalx = ((current[0] + move[0]) >= 0 ) and ((current[0] + move[0]) < map_size[0])
			legaly = ((current[1] + move[1]) >= 0 ) and ((current[1] + move[1]) < map_size[1])
			avoid_walls = [current[0] + move[0], current[1] + move[1]] not in walls
			avoid_pits = [current[0] + move[0], current[1] + move[1]] not in pits
			legal = legalx and legaly and avoid_walls and avoid_pits
			#print "last_dist:", last_dist
			#print "dist:", dist
			#print "legalx", legalx
			#print"legaly", legaly
			#print "avoid_walls", avoid_walls
			#print "avoid_pits", avoid_pits
			if ( (dist <= last_dist) and legal ):
				next_move[0] = current[0] + move[0]
				next_move[1] = current[1] + move[1]
				last_dist = dist
				#print "next_move_x", current[0] + move[0]
				#print "next_move_y", current[1] + move[1]
		current[0] = next_move[0]
		current[1] = next_move[1]
		opt_list.append(deepcopy(current))
		index += 1
		#print "index", index
		#print "currentx:", current[0]
		#print "currenty:", current[1]
		#print 
	return opt_list
