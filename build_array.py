# python build_array.py
# cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
import os
import shutil
import numpy as np
from scipy.optimize import curve_fit
#### read envi image
import spectral.io.envi as envi
from spectral import *
import cv2
    # need to find the path first
    # locate the target folder 
folder = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/SS' 
# this path should be the location of your folders (check hackmd).
date = os.listdir(folder)
#### find the number of row and colume
standard_img = envi.open('D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/Decay/20150813/20150813_0_SS.hdr')
# the meaning of standard_img is to load the size of your images. Select any of your images.
standard_load = standard_img.load()
row = standard_load.shape[0]
col = standard_load.shape[1]

    #####fist loop: enter the second folder
# create a matrix to store time series
t_matrix = []
for i in range(19):
    for j in range(8):
        if i != 4 and i!= 5 and i!= 6 and i!=11 and i!= 12 and i!= 13 and i != 14:
            t_matrix.append(24*i+j)
# t_matrix is used to restore the corresponding hour of your images.
# If you need to change t_matrix, you can also use this way to write: t_matrix = [0,1,2,3,....]
total_image_num = len(date)*8 # because GOCI have 8 images per day, change this if you use a different satellite
img_matrix = np.zeros((total_image_num, row, col)) # build a 3D array like array[t][x][y]
img_index = 0 # The depth index of image matrix, i.e. how many t in the array

for date in date:
    for h in range(8):# find the complete file path, change 8 into other number if you use different satellite
        # print(t,img_index)
        ss_file = folder + '/'+ date+'/' +date + '_' + str(h) + '_SS.hdr'
        print(ss_file) # prove that each file is found        
        
        data = envi.open(ss_file)
        img = data.read_band(0)
        img_matrix[img_index] = img
        img_index = img_index + 1 
            
# print(img_matrix.shape)
def image_statistic(img_matrix,img_row,img_col):
    #### generate mean and variance
    img_mean = np.zeros((row, col))
    img_variance = np.zeros((row, col))
    img_max_difference = np.zeros((row, col))
#### input a 3D array, make it into 2D image
    for i in range(row):
        for j in range(col):
            m_temp = []
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    m_temp.append(img_matrix[t][i][j])
            if len(m_temp)>3:
                img_mean[i][j] = np.mean(m_temp)
                img_variance[i][j] = np.var(m_temp)
                img_max_difference[i][j] = max(m_temp)-min(m_temp)
            

    ####Save as image in ENVI format
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/Mean.hdr', img_mean)
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/Variance.hdr', img_variance)
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/max_difference.hdr', img_max_difference)
def regression_form(t,a,b,c):
    with np.errstate(divide = 'ignore'):
        s = np.float64(a*np.exp(-1*b*t)+c)
    return s

def regression_form2(t,a,b,):
    # this form contain only 2 variable
    with np.errstate(divide = 'ignore'):
        s = np.float64(a*np.exp(-1*b*t))
    return s

# we choose regression 5 and 6 for now
"""
def do_regression(img_matrix, t_matrix,row,col):
    # start from the point right after the max point.
    a_matrix = np.zeros((row, col))
    b_matrix = np.zeros((row, col))
    c_matrix = np.zeros((row, col))
    ls = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ss_temp = []
            t_temp = [] #this array restore the hour 
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    ss_temp.append(img_matrix[t][i][j]) # temporary matrix to secure the sequence of value in different time
                    t_temp.append(t_matrix[t]) # temporary matrix to secure the hours correlate to the m_temp
            ## find the max value
            t_use = [] # matrix used to regression
            ss_use = []

            if len(t_temp) >5:
                for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    t_use.append(t_temp[n])
                    ss_use.append(ss_temp[n])
                            # regression: concentration = a*e^(-b*t)

                    
            if len(t_use)>5 :
                c_matrix[i][j] =min(ss_use) ## let c = min(ss_use)
                for k in range(len(ss_use)):
                    ss_use[k] = ss_use[k] - min(ss_use)
                 # regression: concentration = a*e^(-b*t)+c
            if len(t_use)>5 :

                try:
                    [popt, pcov] = curve_fit(regression_form, t_use, ss_use,maxfev = 50,p0=[5,0.011],bounds=(0,[15,20]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                except:
                    a_matrix[i][j] = 0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue
                for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    y = np.float64(a_matrix[i][j]*np.exp(-1*b_matrix[i][j]*t_temp[n])+c_matrix[i][j])
                    ls[i][j] = ls[i][j] + np.power((y-ss_temp[n]),2)                   
    envi.save_image('a_fixc.hdr', b_matrix)
    envi.save_image('b_fixc.hdr', b_matrix)
    envi.save_image('c_fixc.hdr', c_matrix)
    envi.save_image('least_square_fixc.hdr', ls)
"""
"""
def do_regression2(img_matrix, t_matrix,row,col):
    ## use all points
    a_matrix = np.zeros((row, col))
    b_matrix = np.zeros((row, col))
    c_matrix = np.zeros((row, col))
    ls = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ss_use = []
            t_use = []
            ss_temp = []
            t_temp = [] #this array restore the hour 
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    ss_temp.append(img_matrix[t][i][j]) # temporary matrix to secure the sequence of value in different time
                    t_temp.append(t_matrix[t]) # temporary matrix to secure the hours correlate to the m_temp

            if len(t_temp)>5 :
                for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    t_use.append(t_temp[n])
                    ss_use.append(ss_temp[n])
                try:
                    [popt, pcov] = curve_fit(regression_form, t_temp, ss_temp,maxfev = 1000,p0=[13,0.011,1],bounds=(0,[np.inf,np.inf,10]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                    c_matrix[i][j] = popt[2]                    
                except:
                    a_matrix[i][j] = 0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue
                for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    y = np.float64(a_matrix[i][j]*np.exp(-1*b_matrix[i][j]*t_temp[n])+c_matrix[i][j])
                    ls[i][j] = ls[i][j] + np.power((y-ss_temp[n]),2)
    envi.save_image('a_all.hdr', b_matrix)
    envi.save_image('b_all.hdr', b_matrix)
    envi.save_image('c_all.hdr', c_matrix)
    envi.save_image('least_square_all.hdr', ls)
"""
"""
def do_regression3(img_matrix, t_matrix,row,col):
    # do regression from higher but not highest value by using threshold
    a_matrix = np.zeros((row, col))
    b_matrix = np.zeros((row, col))
    c_matrix = np.zeros((row, col))
    num =0
    for i in range(row):
        for j in range(col):
            ss_temp = []
            t_temp = [] #this array restore the hour 
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    ss_temp.append(img_matrix[t][i][j]) # temporary matrix to secure the sequence of value in different time
                    t_temp.append(t_matrix[t]) # temporary matrix to secure the hours correlate to the m_temp
            
            
            ## define threshold
            n = 0
            
            ss_use =[]
            t_use=[]
            if len(ss_temp)>5:
                threshold = 0.8*np.mean(ss_temp)
            
                for k in range(len(ss_temp)):
                    if ss_temp[k]<threshold:
                        n = n+1
                    else:
                        break

                for k in range(n,len(ss_temp)):
                    ss_use.append(ss_temp[k])
                    t_use.append(t_temp[k])
            if len(t_use)>5 :
                for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    t_use.append(t_temp[n])
                    ss_use.append(ss_temp[n])
                try:
                    [popt, pcov] = curve_fit(regression_form, t_use, ss_use,maxfev = 1000,p0=[13,0.011,1],bounds=(0,[np.inf,np.inf,10]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                    c_matrix[i][j] = popt[2]
                    num = num+1
                except:
                    a_matrix[i][j] = 0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue
    print('num:',num)
    return a_matrix, b_matrix, c_matrix

def do_regression4(img_matrix, t_matrix,row,col):
    # start from the point right after the max point.
    a_matrix = np.zeros((row, col))
    b_matrix = np.zeros((row, col))
    c_matrix = np.zeros((row, col))
    ls = np.zeros((row, col))

    for i in range(row):
        for j in range(col):


            ss_temp = []
            t_temp = [] #this array restore the hour 
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    ss_temp.append(img_matrix[t][i][j]) # temporary matrix to secure the sequence of value in different time
                    t_temp.append(t_matrix[t]) # temporary matrix to secure the hours correlate to the m_temp
            ## find the max value
            t_use = [] # matrix used to regression
            ss_use = []
            if len(t_temp) >5:
                for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    t_use.append(t_temp[n])
                    ss_use.append(ss_temp[n])
                            # regression: concentration = a*e^(-b*t)+c
            if len(t_use)>5 :
                try:
                    [popt, pcov] = curve_fit(regression_form, t_use, ss_use,maxfev = 800,p0=[1,0.011,0.5],bounds=(0,[np.inf,20,10]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                    c_matrix[i][j] = popt[2]
                except:
                    a_matrix[i][j] = 0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue
                # for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    # y = np.float64(a_matrix[i][j]*np.exp(-1*b_matrix[i][j]*t_temp[n])+c_matrix[i][j])
                    # ls[i][j] = ls[i][j] + np.power((y-ss_temp[n]),2)
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/b3.hdr', b_matrix)
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/a3.hdr', a_matrix)
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/c3.hdr', c_matrix)
    # envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/least_square_new_800.hdr', ls)
"""

def do_regression5(img_matrix, t_matrix,row,col):
    # start from the point right after the max point for problematic area.
    a_matrix = np.zeros((row, col))
    b_matrix = np.zeros((row, col))
    c_matrix = np.zeros((row, col))
    ls = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ss_temp = []
            t_temp = [] #this array restore the hour 
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    ss_temp.append(img_matrix[t][i][j]) # temporary matrix to secure the sequence of value in different time
                    t_temp.append(t_matrix[t]) # temporary matrix to secure the hours correlate to the m_temp
            ## find the max value
            t_use = [] # matrix used to regression
            ss_use = []
            if len(t_temp) >5:
                for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                    t_use.append(t_temp[n])
                    ss_use.append(ss_temp[n])
                            # regression: concentration = a*e^(-b*t)+c
            if len(t_use)>5 :
                try:
                    [popt, pcov] = curve_fit(regression_form, t_use, ss_use,maxfev = 200,p0=[1,0.011,ss_use[len(ss_use)-1]],bounds=([0,0,0.5],[np.inf,1.5,10]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                    c_matrix[i][j] = popt[2]
                    
                    for n in range(ss_temp.index(max(ss_temp))+1, len(ss_temp)):
                        y = np.float64(a_matrix[i][j]*np.exp(-1*b_matrix[i][j]*t_temp[n])+c_matrix[i][j])
                        ls[i][j] = ls[i][j] + np.power((y-ss_temp[n]),2)

                except:
                    a_matrix[i][j] =0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue

    envi.save_image('a2.hdr', b_matrix)
    envi.save_image('b2.hdr', b_matrix)
    envi.save_image('c2.hdr', c_matrix)
    # envi.save_image('least_square_problem.hdr', ls)

def do_regression6(img_matrix, t_matrix,row,col):
    # start from the point right after the max point for problematic area.
    # t = t -t_max
    a_matrix = np.zeros((row, col))
    b_matrix = np.zeros((row, col))
    c_matrix = np.zeros((row, col))
    ls = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            ss_temp = []
            t_temp = [] #this array restore the hour 
            for t in range(total_image_num):
                if img_matrix[t][i][j] > 0:
                    ss_temp.append(img_matrix[t][i][j]) # temporary matrix to secure the sequence of value in different time
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
                try:
                    [popt, pcov] = curve_fit(regression_form, t_use, ss_use,maxfev = 200,p0=[1,0.1,ss_use[len(ss_use)-1]],bounds=([0,0,0.5],[np.inf,np.inf,10]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                    c_matrix[i][j] = popt[2]

                except:
                    a_matrix[i][j] =0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue

    envi.save_image('a.hdr', b_matrix)
    envi.save_image('b.hdr', b_matrix)
    envi.save_image('c.hdr', c_matrix)
#save array into envi_file:
def save_as_envi(img_matrix,total_image_num):
    # let img_matrix[t][row][col] become img_matrix[row][col][t] because the third index will become the band numbers.
    img_matrix2 = np.zeros([row,col,total_image_num]) # 8 images * 8 days
    for t in range(img_matrix.shape[0]):
        for i in range(img_matrix.shape[1]):
            for j in range(img_matrix.shape[2]):
                img_matrix2[i][j][t] = img_matrix[t][i][j] 
    envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/img_matrix_all.hdr',img_matrix2)
#### execute

########### save image
save_as_envi(img_matrix,total_image_num)
########### statistic
image_statistic(img_matrix,row,col)
########### regression
do_regression5(img_matrix,t_matrix,row,col)
