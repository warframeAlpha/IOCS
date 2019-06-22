# pro build_array.py
# cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
import os
import shutil
import numpy as np
from scipy.optimize import curve_fit
#### read envi image
import spectral.io.envi as envi
from spectral import *
import csv
    # need to find the path first
    # locate the target folder 
folder = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/decay' # change this path if u want.
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
        # print(t,img_index)
        ss_file = folder + '/'+ date+'/' +date + '_' + str(h) + '_SS.hdr'
        print(ss_file) # prove that each file is found        
        
        data = envi.open(ss_file)
        img = data.read_band(0)
        img_matrix[img_index] = img
        t_martix.append(t) 
        img_index = img_index + 1 # change into next layer
            
        t = t + 1 
    t = t + 16
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
    envi.save_image('Mean.hdr', img_mean)
    envi.save_image('Variance.hdr', img_variance)
    envi.save_image('max_difference.hdr', img_max_difference)
def regression_form(t,a,b,c):
    with np.errstate(divide = 'ignore'):
        s = np.float64(a*np.exp(-1*b*t)+c)
    return s
def regression_form2(t,b,c):
    # this form contain only 2 variable
    with np.errstate(divide = 'ignore'):
        s = np.float64(10*np.exp(-1*b*t)+c)
    return s

def do_regression(img_matrix, t_martix,row,col):
    # start from the point right after the max point.
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
                    [popt, pcov] = curve_fit(regression_form, t_use, ss_use,maxfev = 50,p0=[5,0.011,1],bounds=(0,[15,20,10]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                    c_matrix[i][j] = popt[2]
                except:
                    a_matrix[i][j] = 0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue
    envi.save_image('b.hdr', b_matrix)
    envi.save_image('a.hdr', a_matrix)
    envi.save_image('c.hdr', c_matrix)

            # print(t_temp)
            ############ write a csv file to help us define the initial guess
            # if i == 100 and j == 100:
            #     with open('regression.csv','w') as csvfile:
            #         save = csv.writer(csvfile, delimiter = ',')
            #         save.writerow(t_use)
            #         save.writerow(ss_use)            


    return a_matrix, b_matrix, c_matrix


def do_regression2(img_matrix, t_martix,row,col):
    ## use all points
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

            if len(t_temp)>5 :
                try:
                    [popt, pcov] = curve_fit(regression_form, t_temp, ss_temp,maxfev = 1000,p0=[13,0.011,1],bounds=(0,[np.inf,np.inf,10]))
                    a_matrix[i][j] = popt[0]
                    b_matrix[i][j] = popt[1]
                    c_matrix[i][j] = popt[2]
                    if b_matrix[i][j]<0:
                        a_matrix[i][j] = 0
                        b_matrix[i][j] = 0
                        c_matrix[i][j] = 0                        
                except:
                    a_matrix[i][j] = 0
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue

    return a_matrix, b_matrix, c_matrix

def do_regression3(img_matrix, t_martix,row,col):
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
                    t_temp.append(t_martix[t]) # temporary matrix to secure the hours correlate to the m_temp
            
            
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
                try:
                    [popt, pcov] = curve_fit(regression_form, t_use, ss_use,maxfev = 1000,p0=[13,0.011,1],bounds=([0,0,0],[np.inf,np.inf,8]))
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

def do_regression4(img_matrix, t_martix,row,col):
    # start from the point right after the max point and let a =10.
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
                    [popt, pcov] = curve_fit(regression_form2, t_use, ss_use,maxfev = 1000,p0=[0.011,1],bounds=(0,[np.inf,10]))
                    b_matrix[i][j] = popt[0]
                    c_matrix[i][j] = popt[1]
                except:
                    b_matrix[i][j] = 0
                    c_matrix[i][j] = 0
                    continue

    envi.save_image('b_reg4.hdr', b_matrix)
    envi.save_image('c_reg4.hdr', c_matrix)


#save array into envi_file:
def save_as_envi(img_matrix):
    # let img_matrix[t][row][col] become img_matrix[row][col][t] because the third index will become the band numbers.
    img_matrix2 = np.zeros([488,570,56])
    for t in range(img_matrix.shape[0]):
        for i in range(img_matrix.shape[1]):
            for j in range(img_matrix.shape[2]):
                img_matrix2[i][j][t] = img_matrix[t][i][j] 
    envi.save_image('img_matrix2.hdr',img_matrix2)
#### execute

########### save image
# save_as_envi(img_matrix)
########### statistic
# image_statistic(img_matrix,row,col)
########### regression
# do_regression(img_matrix,t_martix,row,col)

# result = do_regression(img_matrix,t_martix,row,col)
# a_matrix = result[0]
# b_matrix = result[1]
# c_matrix = result[2]
# ############ export data
# envi.save_image('b.hdr', b_matrix)
# envi.save_image('a.hdr', a_matrix)
# envi.save_image('c.hdr', c_matrix)
# with open('t_matrix.csv','w') as csvfile:
#     save = csv.writer(csvfile, delimiter = ',')
#     save.writerow(t_martix)

do_regression(img_matrix,t_martix,row,col)