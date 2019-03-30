import envipyengine
envipyengine.config.set('engine', 'C:/Program Files/Exelis/IDL82/bin/bin.x86')

from envipyengine import Engine
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor

import os
m = np.zeros((2,3,4))
z = np.ones((3,4))
m1 = np.append(m,z) #result = [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
m2 = np.dstack((m,z))# result = ValueError: all the input array dimensions except for the concatenation axis must match exactly
