#!/usr/bin/env python
#robot.py implementation goes here

import rospy
import json
from std_msgs.msg import String, Float32, Bool
from cse_190_assi_3.msg import AStarPath, PolicyList
from read_config import read_config
import image_util as iu
import astar
import mdp
import plearn
import alearn
import data_transcriber as dt
import numpy as np
import math as m

class Robot():
	def __init__(self):
		rospy.init_node("Robot")
		self.config = read_config()
		#Publishers
		self.results_AStar_pub = rospy.Publisher("/results/path_list", 
			AStarPath, 
			queue_size=10, 
			latch=True
		)
		self.results_MDP_pub = rospy.Publisher("/results/policy_list",
			PolicyList,
			queue_size=10,
			latch=True
		)
		self.sim_complete_pub = rospy.Publisher("/map_node/sim_complete",
			Bool,
			queue_size=10,
			latch=True
		)
		#A* Inputs
		self.move_list = self.config["move_list"]
		self.map_size = self.config["map_size"]
		self.start = self.config["start"]
		self.goal = self.config["goal"]
		self.walls = self.config["walls"]
		self.pits = self.config["pits"]
		#MDP Inputs
		#probabilities
		self.p_f = self.config["prob_move_forward"]
		self.p_b = self.config["prob_move_backward"]
		self.p_l = self.config["prob_move_left"]
		self.p_r = self.config["prob_move_right"]
		#rewards
		self.r_step = self.config["reward_for_each_step"]
		self.r_wall = self.config["reward_for_hitting_wall"]
		self.r_goal = self.config["reward_for_reaching_goal"]
		self.r_pit = self.config["reward_for_falling_in_pit"]
		#iteration
		max_iterations = self.config["max_iterations"]
		threshold_difference =self.config["threshold_difference"]
		index = 0		
		last_reward = 1
		this_reward = 0
		opt_move = AStarPath()
		#self.p_learning = self.config["p_learning"]
		#self.a_learning = self.config["a_learning"]
		#pLearn
		plearn.p_learn()
		#aLearn
		alearn.a_learn()
		#A*
		rospy.sleep(0.1)
		opt_path = astar.a_opt_search()
		for move in opt_path:
			opt_move.data = move
			rospy.sleep(0.1)
			self.results_AStar_pub.publish(opt_move)
		#MDP
		opt_policy = PolicyList()
		opt_policy.data = mdp.m_opt_search()
		self.results_MDP_pub.publish(opt_policy)
		rospy.sleep(0.1)
		#Sim Complete
		rospy.sleep(1)
		self.sim_complete_pub.publish(True)
		rospy.sleep(1)
		rospy.signal_shutdown(True)

if __name__ == '__main__':
	robot = Robot()

