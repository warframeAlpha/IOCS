# python compare.py
#cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
#This script is designed to compare two results from different methods by plotting 2 results and original data together.
import numpy as np
import spectral.io.envi as envi
from spectral import *
import os
import shutil
import matplotlib.pyplot as plt
import cv2
import pandas as pd
# read results from different methods and read the original data
img= envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/img_matrix2.hdr')
img_matrix = img.load()
img_matrix = img_matrix.read_bands(range(0,img_matrix.shape[2]))
# read_all
a_all = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a_all.hdr')
b_all = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_all.hdr')
c_all = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_all.hdr')
a_all = a_all.load()
a_all = a_all.read_band(0)
b_all = b_all.load()
b_all = b_all.read_band(0)
c_all = c_all.load()
c_all = c_all.read_band(0)
# read_max+1
a_max1 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a_max+1.hdr')
b_max1 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_max+1.hdr')
c_max1 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_max+1.hdr')
a_max1 = a_max1.load()
a_max1 = a_max1.read_band(0)
b_max1 = b_max1.load()
b_max1 = b_max1.read_band(0)
c_max1 = c_max1.load()
c_max1 = c_max1.read_band(0)
# read reg4: a = 10
b_reg4 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_all.hdr')
c_reg4 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_all.hdr')
b_reg4 = b_reg4.load()
b_reg4 = b_reg4.read_band(0)
c_reg4 = c_reg4.load()
c_reg4 = c_reg4.read_band(0)
### read time_matrix (hours)
t_temp = pd.read_csv('D:/HOMEWORK/rslab/IOCS_2019/regression/t_matrix.csv')
t_matrix = []
for col in t_temp:
    t_matrix.append(int(col))
# plot
def plot1(a_all,b_all,c_all,a_max1,b_max1,c_max1,img_matrix,t_matrix):
    ## plot a single pixel
    plt.scatter(t_matrix,img_matrix[1][1])
    x = np.linspace(0,156,num=200)
    y1 = a_all[1][1]*np.exp(-b_all[1][1]*x)+c_all[1][1]
    y2 = a_max1[1][1]*np.exp(-b_max1[1][1]*x)+c_max1[1][1]
    plt.plot(x,y1,label ='y1' )
    plt.plot(x,y2,label ='y2')
    plt.ylim([0,20])
    plt.legend()
    plt.show()

def plot_all(a_all,b_all,c_all,a_max1,b_max1,c_max1,b_reg4,c_reg4,img_matrix,t_matrix):
    # plot all pixels
    x = np.linspace(0,156,num=200)
    for i in range(0,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            plt.scatter(t_matrix,img_matrix[i][j])
            y1 = a_all[i][j]*np.exp(-b_all[i][j]*x)+c_all[i][j]
            y2 = a_max1[i][j]*np.exp(-b_max1[i][j]*x)+c_max1[i][j]
            y3 = 10*np.exp(-b_reg4[i][j]*x)+c_reg4[i][j]
            plt.plot(x,y1,label ='all' )
            plt.plot(x,y2,label ='max+1')
            plt.plot(x,y3,label = 'reg4')
            plt.ylim([0,20])
            plt.legend()
            fname = 'F:/Endz_Research_data/reg4/'+'i_'+str(i)+'j_'+str(j)+'.png' 
            plt.savefig(fname)
            plt.clf()

def plot_part(a_all,b_all,c_all,a_max1,b_max1,c_max1,b_reg4,c_reg4,img_matrix,t_matrix):
    # plot the area with problems
    x = np.linspace(0,156,num=200)
    for i in range(197,340):
        for j in range(100,180):
            plt.scatter(t_matrix,img_matrix[i][j])
            y1 = a_all[i][j]*np.exp(-b_all[i][j]*x)+c_all[i][j]
            y2 = a_max1[i][j]*np.exp(-b_max1[i][j]*x)+c_max1[i][j]
            y3 = 10*np.exp(-b_reg4[i][j]*x)+c_reg4[i][j]
            plt.plot(x,y1,label ='all'+'b_'+str(b_all[i][j])+'c_'+str(c_all[i][j]))
            plt.plot(x,y2,label ='max+1'+'b_'+str(b_max1[i][j])+'c_'+str(c_max1[i][j]))
            plt.plot(x,y3,label = 'reg4'+'b_'+str(b_reg4[i][j])+'c_'+str(c_reg4[i][j]))
            plt.ylim([0,20])
            plt.legend()
            fname = 'F:/Endz_Research_data/problem/'+'i_'+str(i)+'j_'+str(j)+'.png' 
            plt.savefig(fname)
            plt.clf()
def save_as_tiff(a_matrix,b_matrix,c_matrix):
    cv2.imwrite('a_tiff.tiff',a_matrix)
    cv2.imwrite('b_tiff.tiff',b_matrix)
    cv2.imwrite('c_tiff.tiff',c_matrix)
    
## execute1
save_as_tiff(a_max1,b_max1,c_max1)