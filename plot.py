# python plot.py
#cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
# This code is designed to batch generate the figure after exponential regression
import numpy as np
import spectral.io.envi as envi
from spectral import *
import os
import shutil
import matplotlib.pyplot as plt
import csv
import pandas as pd

#### load image as matrix
img= envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/img_matrix2.hdr')
img_matrix = img.load()
img_matrix = img_matrix.read_bands(range(0,img_matrix.shape[2]))
a = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a.hdr')
b = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b.hdr')
c = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c.hdr')
a_matrix = a.load()
a_matrix = a_matrix.read_band(0)
b_matrix = b.load()
b_matrix = b_matrix.read_band(0)
c_matrix = c.load()
c_matrix = c_matrix.read_band(0)
### read time_matrix (hours)
t_temp = pd.read_csv('D:/HOMEWORK/rslab/IOCS_2019/regression/t_matrix.csv')
t_matrix = []
for col in t_temp:
    t_matrix.append(int(col))

# print(t_matrix)

####start to plot
def plot2(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix):
    ## plot a single figure
    plt.scatter(t_matrix,img_matrix[1][1])
    # plt.hold(True)
    x = np.linspace(0,156,num=200)
    y = a_matrix[1][1]*np.exp(-b_matrix[1][1]*x)+c_matrix[1][1]
    plt.plot(x,y)
def plot_all(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix):
    # plot all figure in normal scale
    x = np.linspace(0,156,num=200)
    for i in range(0,img_matrix.shape[0],8):
        for j in range(0,img_matrix.shape[1],10):
            plt.scatter(t_matrix,img_matrix[i][j])
            threshold = np.mean(b_matrix)+2*np.std(b_matrix)
            if b_matrix[i][j]<threshold:
                y = a_matrix[i][j]*np.exp(-b_matrix[i][j]*x)+c_matrix[i][j]
                plt.plot(x,y)
                plt.ylim([0,30])
            fname = 'D:/HOMEWORK/rslab/IOCS_2019/regression/fig/'+'i_'+str(i)+'j_'+str(j)+'.png'
            plt.savefig(fname)
            plt.clf()
def plot_log_all(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix):
    # plot all figure in log scale
    x = np.linspace(0,156,num=200)
    for i in range(0,img_matrix.shape[0],8):
        for j in range(0,img_matrix.shape[1],10):
            plt.scatter(t_matrix,img_matrix[i][j])
            threshold = np.mean(b_matrix)+2*np.std(b_matrix)
            if b_matrix[i][j]<threshold:
                y = a_matrix[i][j]*np.exp(-b_matrix[i][j]*x)+c_matrix[i][j]
                plt.plot(x,y)
                plt.yscale('log')
            fname = 'D:/HOMEWORK/rslab/IOCS_2019/regression/fig/'+'i_'+str(i)+'j_'+str(j)+'.png'
            plt.savefig(fname)
            plt.clf()
### execute
# plot2(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix)
# plt.savefig('testfigure.png')
# plt.show()
plot_all(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix)
# print(np.amin(b_matrix))
# print(np.amax(b_matrix))
# print(np.mean(b_matrix))
# print(np.std(b_matrix))
