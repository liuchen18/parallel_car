#!/usr/bin/env python 

import rospy

import numpy as np

from numpy import sin, cos

class GradientOptimizer:
    """
    A class to perform gradient optimization for both car movement and wx rotation
    """
    def __init__(self, car_weight=1.0, wx_weight=1.0, pole_weight=1.0, car_rate=1.0, wx_rate=1.0):
        """Construction function for gradient optimizer
        
        Keyword Arguments:
            car_weight {float} -- car (mobile base) weight in cost function, applied to car's cost considering translation in x, y and rotation in yaw (default: {1.0})
            wx_weight {float} -- wx weight in cost function, applied to wx's cost considering rotation between wx_link and up_link (default: {1.0})
            pole_weight {float} -- pole weight in cost function, applied to poles' cost considering pole length (default: {1.0})
            car_rate {float} -- [description] (default: {1.0})
            wx_rate {float} -- [description] (default: {1.0})
        """
        self._car_weight = car_weight
        self._wx_weight = wx_weight
        self._pole_weight = pole_weight
        self._car_rate = car_rate
        self._wx_rate = wx_rate

    def compute_cost(self, parallel_increment, pole_length_list, old_pole_length_list):
        """A function to compute the cost of a potential pose of the parallel_car
        
        Arguments:
            parallel_increment {ParallelPose} -- the desired incremental position of the parallel car
            pole_length_list {list} -- the length of the poles at the desired pose of the parallel mechanism 
            old_pole_length_list {list} -- the length of the poles at the previous namingly optimized pose of the parallel mechanism
        
        Returns:
            [double] -- the total cost for the desired incremental pose of the parallel_car
        """
        delta_x = parallel_increment.x
        delta_y = parallel_increment.y
        delta_theta = parallel_increment.theta
        delta_alpha = parallel_increment.alpha

        car_cost = np.square(delta_x)+np.square(delta_y)+np.square(delta_theta)
        car_cost *= self._car_weight

        wx_cost = np.square(delta_alpha)
        wx_cost *= self._wx_weight

        pole_cost = 0.0
        for idx in range(0, len(pole_length_list)):
            pole_cost += np.square(pole_length_list[idx]-old_pole_length_list[idx])
        pole_cost *= self._pole_weight

        total_cost = car_cost+wx_cost+pole_cost

        return total_cost