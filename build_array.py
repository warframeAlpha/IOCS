# pro build_array.py
# cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
import os
import shutil
import numpy as np
from scipy.optimize import curve_fit
#### read envi image
import spectral.io.envi as envi
from spectral import *
    # need to find the path first
    # locate the target folder 
folder = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/decay' # 要改
date = os.listdir(folder)
#### find the number of row and colume
standard_img = envi.open('D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/SS/20150803/20150803_0_SS.hdr')
standard_load = standard_img.load()
row = standard_load.shape[0]
col = standard_load.shape[1]

    #####fist loop: enter the second folder
t = 0# set the initial time in hour
t_martix = [] # create a matrix to store time series
total_image_num = len(date)*8 
img_matrix = np.zeros((total_image_num, row, col)) #array[t][x][y]
img_index = 0 # The depth index of image matrix

for date in date:
    for h in range(8):# find the complete file path
        print(t,img_index)
        ss_file = folder + '/'+ date+'/' +date + '_' + str(h) + '_SS.hdr'
        print(ss_file) # prove that each file is found        
        
        data = envi.open(ss_file)
        img = data.read_band(0)
        img_matrix[img_index] = img
        t_martix.append(t) 
        img_index = img_index + 1 # change into next layer
            
        t = t + 1 
    t = t + 16
print(img_matrix.shape)
def image_statistic(img_matrix,img_row,img_col):
    #### generate mean and variance
    img_mean = np.zeros((row, col))
    img_variance = np.zeros((row, col))    
#### input a 3D array, make it into 2D image
    for i in range(row):
        for j in range(col):
            m_temp = []
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    m_temp.append(img_matrix[t][i][j])
            img_mean[i][j] = np.mean(m_temp)
            img_variance[i][j] = np.var(m_temp)

    ####Save as image in ENVI format
    envi.save_image('Mean.hdr', img_mean)
    envi.save_image('Variance.hdr', img_variance)
def regression_form(t,a,b,c):
    with np.errstate(divide = 'ignore'):
        s = a*np.exp(-1*b*t)+c
    return s

def do_regression(img_matrix, t_martix,row,col):
    a_matrix = np.zeros((row, col))
    b_matrix = np.zeros((row, col))
    c_matrix = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ss_temp = []
            t_temp = [] #this array restore the hour 
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    ss_temp.append(img_matrix[t][i][j]) # temporary matrix to secure the sequence of value in different time
                    t_temp.append(t_martix[t]) # temporary matrix to secure the hours correlate to the m_temp
                # regression: concentration = a*e^(-b*t)+c
            [popt, pcov] = curve_fit(regression_form,t_temp,ss_temp)
            a_matrix[i][j] = popt[0]
            b_matrix[i][j] = popt[1]
            c_matrix[i][j] = popt[2]
    return a_matrix, b_matrix, c_matrix
    
#### execute
# image_statistic(img_matrix,row,col)
print(t_martix[20])
result = do_regression(img_matrix,t_martix,row,col)
a_matrix = result[0]
b_matrix = result[1]
c_matrix = result[2]