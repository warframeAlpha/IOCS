# python lmfitt.py
import os
import shutil
import numpy as np
from scipy.optimize import curve_fit
from scipy.optimize import least_squares
import lmfit
from lmfit import Parameters, Minimizer
import spectral.io.envi as envi
from spectral import *
# read images as a np_array
img= envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/img_matrix_all.hdr')
img_matrix = img.load()
img_matrix = img_matrix.read_bands(range(0,img_matrix.shape[2]))
[row, col] =[img_matrix.shape[0], img_matrix.shape[1]] 
# define t_matrix
t_matrix = []
for i in range(19):
    for j in range(8):
        if i != 4 and i!= 5 and i!= 6 and i!=11 and i!= 12 and i!= 13 and i != 14:
            t_matrix.append(24*i+j)
# try scipy.optimize.least_square
## regression function
def residual(x,a,b,c,data):
    model = a * np.exp(-b*x) + c
    return abs(model - data)

def func(pars, x, data=None):
    a, b, c = pars['a'], pars['b'], pars['c']
    with np.errstate(divide = 'ignore'):
        s = np.float64(a*np.exp(-1*b*t)+c)
        res = abs(s - data)
    return res
def dfunc(pars, x, data=None):
    a, b = pars['a'], pars['b']
    v = np.exp(-b*x)
    return np.array([v, -a*x*v, np.ones(len(x))])
ya = 0
fuck = 0
## method
a_matrix = np.zeros((row, col))
b_matrix = np.zeros((row, col))
c_matrix = np.zeros((row, col))
for i in range(row):
    for j in range(col):
        ss_temp = []
        t_temp = [] #this array restore the hour 
        for t in range(img_matrix.shape[2]):
            if img_matrix[i][j][t] > 0:
                ss_temp.append(img_matrix[i][j][t]) # temporary matrix to secure the sequence of value in different time
                t_temp.append(t_matrix[t]) # temporary matrix to secure the hours correlate to the m_temp
            ## find the max value
        t_use = [] # matrix used to regression
        ss_use = []
        if len(t_temp) >5:
            for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                t_use.append(t_temp[n]-t_temp[ss_temp.index(max(ss_temp))])
                ss_use.append(ss_temp[n])
                            # regression: concentration = a*e^(-b*t)+c
        if len(t_use)>5 :
            # params = Parameters()
            # params.add('a', value=1, min=0)
            # params.add('b', value=0.1, min = 0)
            # params.add('c', value=ss_use[len(ss_use)-1],min = 0, max=15)
            x = t_use
            data = ss_use
            try:
                # min2 = Minimizer(func, params, args=(x,), kws={'data': data})
                # out2 = min2.leastsq()
                # a_matrix[i][j] = out2.params['a']
                # b_matrix[i][j] = out2.params['b']
                # c_matrix[i][j] = out2.params['c']
                ya = ya +1
            except:
                a_matrix[i][j] = -1
                b_matrix[i][j] = -1
                c_matrix[i][j] = -1
                fuck = fuck +1
                continue

envi.save_image('a_lmfit.hdr', b_matrix)
envi.save_image('b_lmfit.hdr', b_matrix)
envi.save_image('c_lmfit.hdr', c_matrix)
print('ya:', ya)
print('fuck:', fuck)