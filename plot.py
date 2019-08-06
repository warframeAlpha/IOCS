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
a = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a_800.hdr')
b = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_800.hdr')
c = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_800.hdr')
a_matrix = a.load()
a_matrix = a_matrix.read_band(0)
b_matrix = b.load()
b_matrix = b_matrix.read_band(0)
c_matrix = c.load()
c_matrix = c_matrix.read_band(0)
### read time_matrix (hours)
t_temp = pd.read_csv('D:/HOMEWORK/rslab/IOCS_2019/regression/t_matrix.csv')
t_matrix = [0,1,2,3,4,5,6,7,24,25,26,27,28,29,30,31,48,49,50,51,52,53,54,55,72,73,74,75,76,77,78,79,192,193,194,195,196,197,198,199,
216,217,218,219,220,221,222,223,240,241,242,243,244,245,246,247,264,265,266,267,268,269,270,271]

# print(t_matrix)

####start to plot
def plot2(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix):
    ## plot a single figure

    plt.figure(figsize=(20,10))
    plt.title('regression result',fontsize = 40)
    plt.scatter(t_matrix,img_matrix[1][1])
    # plt.hold(True)
    x = np.linspace(0,271,num=300)
    y = a_matrix[1][1]*np.exp(-b_matrix[1][1]*x)+c_matrix[1][1]
    plt.plot(x,y)
    plt.xlabel('t (hours)',fontsize = 30)
    plt.ylabel('SS concentration (g/cm^3)', fontsize = 30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.show()
def plot_all(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix):
    # plot all figure in normal scale
    x = np.linspace(0,156,num=200)
    for i in range(0,img_matrix.shape[0],8):
        for j in range(0,img_matrix.shape[1],10):
            plt.scatter(t_matrix,img_matrix[i][j])
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
def plot3(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix):
    # plot 3 regression lines in one figure
    x = np.linspace(0,272,num=300)
    row = [100,122,112]
    col = [299,295,201]
    line = ['mo','co','bo']

    plt.scatter(t_matrix,img_matrix[100][299],marker='x',color = 'm')
    plt.scatter(t_matrix,img_matrix[122][295],marker='x',color = 'c')
    plt.scatter(t_matrix,img_matrix[112][201],marker='x',color = 'b')
    
    plt.legend()
    plt.show()
   
def plot4(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix):
    # plot 3 regression lines in one figure
    x = np.linspace(0,272,num=300)

    plt.scatter(t_matrix,img_matrix[181][314],marker='x',color = 'r')
    plt.scatter(t_matrix,img_matrix[160][294],marker='x',color = 'orange')
    # plt.scatter(t_matrix,img_matrix[112][201],marker='x',color = 'b')
    
    plt.legend()
    plt.show()
   
### execute
# plot2(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix)
# plt.savefig('testfigure.png')
# plt.show()
plot4(a_matrix,b_matrix,c_matrix,img_matrix,t_matrix)
# print(np.amin(b_matrix))
# print(np.amax(b_matrix))
# print(np.mean(b_matrix))
# print(np.std(b_matrix))
