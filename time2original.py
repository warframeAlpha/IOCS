# python time2original.py
# cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
# This file is used to compute how long each pixel takes to their original state
## read images
import numpy as np
import spectral.io.envi as envi
from scipy.optimize import fsolve
from spectral import *
import os
import shutil
import matplotlib.pyplot as plt
import cv2

## read images
img= envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/img_matrix2.hdr')
img_matrix = img.load()
img_matrix = img_matrix.read_bands(range(0,img_matrix.shape[2]))
## read a b c (regression result)
a = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/a.hdr')
b = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/b.hdr')
c = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/c.hdr')
a = a.load()
a = a.read_band(0)
b = b.load()
b = b.read_band(0)
c = c.load()
c = c.read_band(0)
## read statistic result
max_variation = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/max_difference.hdr')
max_variation = max_variation.load()
max_variation = max_variation.read_band(0)
## read 4-days mean image
init_state = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/0804_0807_mean.hdr')
init_state = init_state.load()
init_state = init_state.read_band(0)
## read time_matrix (hours)
t_matrix = [0,1,2,3,4,5,6,7,24,25,26,27,28,29,30,31,48,49,50,51,52,53,54,55,72,73,74,75,76,77,78,79,192,193,194,195,196,197,198,199,
216,217,218,219,220,221,222,223,240,241,242,243,244,245,246,247,264,265,266,267,268,269,270,271]
## def the function for fsolve
def f(t,p):
    a=p[0]
    b=p[1]
    c = p[2]
    threshold = p[3]
    return a*np.exp(-b*t)+c-threshold
## Now we choose compute_t4
def compute_t(a_50,b_50,c_50,img_matrix,t_matrix,init_state):
    k = 0.1
    t_method = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_decay = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    ss_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))

    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            threshold = k*max_variation[i][j] + c_50[i][j]
            if b_50[i][j]!=0:
                t0 = fsolve(f,0,[a_50[i][j],b_50[i][j],c_50[i][j],threshold])
                t_method[i][j] = t0
                indexx = np.argmax(img_matrix[i][j])
                t_max[i][j] = t_matrix[indexx]
                ss_max[i][j] = img_matrix[i][j][indexx]

                t_decay[i][j] = t_method[i][j] - t_max[i][j]
            if t0 <=0 or t_decay[i][j]<0:
                t_method[i][j] = -1
                t_decay[i][j] = -1
    # envi.save_image('t_method1_01.hdr', t_method)
    # envi.save_image('t_max1_01.hdr', t_max)
    # envi.save_image('t_decay1_01.hdr', t_decay)
    envi.save_image('ss_max.hdr', ss_max)

    
def compute_t2(a_50,b_50,c_50,img_matrix,t_matrix,init_state):
    # threshold is based on 4 days mean
    k = 0.1
    t_method = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_decay = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            threshold = k*max_variation[i][j] + init_state[i][j]
            if b_50[i][j]!=0:
                t0 = fsolve(f,0,[a_50[i][j],b_50[i][j],c_50[i][j],threshold])
                t_method[i][j] = t0
                indexx = np.argmax(img_matrix[i][j])
                t_max[i][j] = t_matrix[indexx]
                t_decay[i][j] = t_method[i][j] - t_max[i][j]
            if t0 <=0 or t_decay[i][j]<0:
                t_method[i][j] = -1
                t_decay[i][j] = -1
    envi.save_image('t_method2_01.hdr', t_method)
    envi.save_image('t_max2_01.hdr', t_max)
    envi.save_image('t_decay2_01.hdr', t_decay)

def compute_t3(a_50,b_50,c_50,img_matrix,t_matrix,init_state):
    # threshold is based on 4 days mean plus a constant
    t_method = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_decay = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            threshold = 0.5 + init_state[i][j]
            if b_50[i][j]!=0:
                t0 = fsolve(f,0,[a_50[i][j],b_50[i][j],c_50[i][j],threshold])
                t_method[i][j] = t0
                indexx = np.argmax(img_matrix[i][j])
                t_max[i][j] = t_matrix[indexx]
                t_decay[i][j] = t_method[i][j] - t_max[i][j]
            if t0 <=0 or t_decay[i][j]<0:
                t_method[i][j] = -1
                t_decay[i][j] = -1
    envi.save_image('t_method3_05.hdr', t_method)
    envi.save_image('t_max3_05.hdr', t_max)
    envi.save_image('t_decay3_05.hdr', t_decay)
def image_stactistic(a_50,b_50,c_50,img_matrix,t_matrix,init_state):
    t_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_min = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    ss_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    ss_min = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    max_avg = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))

    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            
            indexx = np.argmax(img_matrix[i][j])
            t_max[i][j] = t_matrix[indexx]
            ss_max[i][j] = img_matrix[i][j][indexx]
# to avoid seize no data as t_min and ss_min
            img_temp = []
            t_temp = []
            for k in range(len(img_matrix[i][j])):
                if img_matrix[i][j][k] !=0:
                    img_temp.append(img_matrix[i][j][k])
                    t_temp.append(t_matrix[k])
            if len(img_temp)>0:
                indexy = np.argmin(img_temp)
                t_min[i][j] = t_temp[indexy] + 8.5 # because GOCI start from 8:30, but the time start from 0. As for t_max, I use seadas to change that
                ss_min[i][j] = img_temp[indexy]
########################################################
            # max_avg[i][j] = ss_max[i][j]- init_state[i][j]

    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/t_max.hdr', t_max)
    # envi.save_image('t_min.hdr', t_min)
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/ss_max.hdr', ss_max)
    # envi.save_image('ss_min.hdr', ss_min)
    # envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/max-avg.hdr', max_avg)

def compute_t4(a_50,b_50,c_50,img_matrix,t_matrix,init_state):
    # this function is used to fullfish Prof. Wang's request (20190905)
    k1 = 0.5 # the only varibale to adjust
    k2 = 1-k1
    t_method = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_max = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    t_decay = np.zeros((img_matrix.shape[0], img_matrix.shape[1]))
    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            threshold = k1*max_variation[i][j] + k2*init_state[i][j]
            t0 = -1
            if b_50[i][j]!=0:
                t0 = fsolve(f,0,[a_50[i][j],b_50[i][j],c_50[i][j],threshold])
                t_method[i][j] = t0
                indexx = np.argmax(img_matrix[i][j])
                t_max[i][j] = t_matrix[indexx]
                t_decay[i][j] = t_method[i][j] - t_max[i][j]
            if t0 <=0 or t_decay[i][j]<0:
                t_method[i][j] = -1
                t_decay[i][j] = -1
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/td50.hdr', t_method)
    # envi.save_image('t_max2_01.hdr', t_max)
    # envi.save_image('t_decay4_05.hdr', t_decay)
compute_t4(a,b,c,img_matrix,t_matrix,init_state)
# image_stactistic(a,b,c,img_matrix,t_matrix,init_state)