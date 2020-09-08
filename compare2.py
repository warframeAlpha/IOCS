# python compare2.py
#cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
#This script is designed to compare two results from different methods by plotting 2 results and original data together.
import numpy as np
import spectral.io.envi as envi
from scipy.optimize import curve_fit
from spectral import *
import os
import shutil
import matplotlib.pyplot as plt
from pylab import rcParams
import matplotlib as mpl
import cv2
import pandas as pd
# read results from different methods and read the original data
img= envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/img_matrix_all.hdr')
img_matrix = img.load()
img_matrix = img_matrix.read_bands(range(0,img_matrix.shape[2]))
# read_linear
a = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/a_trf.hdr')
b = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/b_trf.hdr')
c = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/c_trf.hdr')
a = a.load()
a = a.read_band(0)
b = b.load()
b = b.read_band(0)
c = c.load()
c = c.read_band(0)
# read_trf_cauchy
a_tc = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/a_trf_cauchy.hdr')
b_tc = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/b_trf_cauchy.hdr')
c_tc = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/c_trf_cauchy.hdr')
a_tc = a_tc.load()
a_tc = a_tc.read_band(0)
b_tc = b_tc.load()
b_tc = b_tc.read_band(0)
c_tc = c_tc.load()
c_tc = c_tc.read_band(0)
# read_trf_soft
a_ts = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/a_trf_soft.hdr')
b_ts = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/b_trf_soft.hdr')
c_ts = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/c_trf_soft.hdr')
a_ts = a_ts.load()
a_ts = a_ts.read_band(0)
b_ts = b_ts.load()
b_ts = b_ts.read_band(0)
c_ts = c_ts.load()
c_ts = c_ts.read_band(0)
# read_Powell
a_ta = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/a_Powell.hdr')
b_ta = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/b_Powell.hdr')
c_ta = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/c_Powell.hdr')
a_ta = a_ta.load()
a_ta = a_ta.read_band(0)
b_ta = b_ta.load()
b_ta = b_ta.read_band(0)
c_ta = c_ta.load()
c_ta = c_ta.read_band(0)
# read_trf_ls
a_tls = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/a_trf_ls.hdr')
b_tls = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/b_trf_ls.hdr')
c_tls = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/c_trf_ls.hdr')
a_tls = a_tls.load()
a_tls = a_tls.read_band(0)
b_tls = b_tls.load()
b_tls = b_tls.read_band(0)
c_tls = c_tls.load()
c_tls = c_tls.read_band(0)
# read_trf_huber
a_th = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/a_trf_huber.hdr')
b_th = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/b_trf_huber.hdr')
c_th = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/c_trf_huber.hdr')
a_th = a_th.load()
a_th = a_th.read_band(0)
b_th = b_th.load()
b_th = b_th.read_band(0)
c_th = c_th.load()
c_th = c_th.read_band(0)

# read t_max
t_max= envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/t_max.hdr')
t_max = t_max.load()
t_max = t_max.read_bands(0)
t_matrix = []
for i in range(19):
    for j in range(8):
        if i != 4 and i!= 5 and i!= 6 and i!=11 and i!= 12 and i!= 13 and i != 14:
            t_matrix.append(24*i+j)
t_matrix2 = []
for i in t_matrix:
    t_matrix2.append(i+8.5)
# t_matrix2 = the really time start from 0:00
day = [0,24,48,72,96,168,192,216,240,264,360,384,408,432,456,500]
total_image_num = len(day)*8  
row = c_tc.shape[0]
col = c_tc.shape[1]

def plot_part(a,b,c,img_matrix,t_matrix,t_max):
    # plot the area with problems
    x = np.linspace(0,500,num=800)
    for i in range(row):
        for j in range(col):
            ss = []
            t = []
            for k in range(len(img_matrix[i][j])):
                if img_matrix[i][j][k]!=0:
                    ss.append(img_matrix[i][j][k])
                    t.append(t_matrix2[k])
            tt = np.linspace(180,460)
            y1 = a[i][j]*np.exp(-b[i][j]*(tt-192))+c[i][j]
            plt.figure(figsize=(25,10))
            plt.scatter(t,ss,s = 200)  
            color_switcher = 0            
            for d in range(len(day)-1):
                if color_switcher ==0:
                    plt.axvspan(day[d],day[d+1],color = '0.5',alpha=0.3)
                    color_switcher = color_switcher+1
                else:
                    plt.axvspan(day[d],day[d+1],color = '0.9',alpha=0.3)
                    color_switcher= color_switcher - 1            
            # plt.title('regression result',fontsize = 50)
            plt.plot(tt,y1,label ='ss = '+str(a[i][j]) + '*exp(-' +str(b[i][j])+'*t)+'+str(c[i][j]),linewidth = 3)
            for pos in ['right','top']:
                plt.gca().spines[pos].set_visible(False)
            for pos in ['left','bottom']:
                plt.gca().spines[pos].set_linewidth(6)

            plt.yticks([0,5,10])
            plt.tick_params(axis = 'both', length = 20, width = 5)
            plt.ylim([0,12])
            plt.xlim([0,500])
            plt.xticks(fontsize=30)            
            plt.yticks(fontsize=30)            
            fname = 'D:/HOMEWORK/rslab/IOCS_2019/figures/trf_cauchy/'+'i_'+str(i)+'j_'+str(j)+'_v10.png' 
            plt.savefig(fname)
            plt.close('all')

def compare(a,b,c,a_ts,b_ts,c_ts,a_tc,b_tc,c_tc,a_ta,b_ta,c_ta,a_tls,b_tls,c_tls,img_matrix,t_matrix,t_max):
    # plot the area with problems
    x = np.linspace(0,500,num=800)
    for i in range(0,1):
        for j in range(255,256):
            ss = []
            t = []
            for k in range(len(img_matrix[i][j])):
                if img_matrix[i][j][k]!=0:
                    ss.append(img_matrix[i][j][k])
                    t.append(t_matrix2[k])
            tt = np.linspace(180,460)
            y1 = a[i][j]*np.exp(-b[i][j]*(tt-192))+c[i][j]
            y2 = a_tc[i][j]*np.exp(-b_tc[i][j]*(tt-168))+c_tc[i][j]
            y3 = a_ts[i][j]*np.exp(-b_ts[i][j]*(tt-168))+c_ts[i][j]
            y4 = a_ta[i][j]*np.exp(-b_ta[i][j]*(tt-168))+c_ta[i][j]
            y5 = a_tls[i][j]*np.exp(-b_tls[i][j]*(tt-168))+c_tls[i][j]
            y6 = a_th[i][j]*np.exp(-b_th[i][j]*(tt-168))+c_th[i][j]
            plt.figure(figsize=(25,10))
            plt.scatter(t,ss,s = 200)  
            color_switcher = 0            
            for d in range(len(day)-1):
                if color_switcher ==0:
                    plt.axvspan(day[d],day[d+1],color = '0.5',alpha=0.3)
                    color_switcher = color_switcher+1
                else:
                    plt.axvspan(day[d],day[d+1],color = '0.9',alpha=0.3)
                    color_switcher= color_switcher - 1            
            # plt.title('regression result',fontsize = 50)
            plt.plot(tt,y1,label ='L-M',linewidth = 3)
            plt.plot(tt,y2,label ='trf_cauchy',linewidth = 3)
            # plt.plot(tt,y3,label ='trf_soft_l1',linewidth = 3)
            plt.plot(tt,y4,label ='Powell',linewidth = 3)
            # plt.plot(tt,y5,label ='trf_ls->soft',linewidth = 3)
            # plt.plot(tt,y6,label ='trf_huber',linewidth = 3)
            plt.legend(fontsize = 20)
            for pos in ['right','top']:
                plt.gca().spines[pos].set_visible(False)
            for pos in ['left','bottom']:
                plt.gca().spines[pos].set_linewidth(6)

            plt.yticks([0,5,10])
            plt.tick_params(axis = 'both', length = 20, width = 5)
            plt.ylim([0,12])
            plt.xlim([0,500])
            plt.xticks(fontsize=30)            
            plt.yticks(fontsize=30)            

            # plt.legend(fontsize = 20)
            # plt.xlabel('t(hours)',fontsize = 50)
            # plt.ylabel('SS(g/m\u00b3)', fontsize = 50)
            # print("The area of your rectangle is {}cm\u00b2".format(area))
            
            # plt.axis('tight')
            fname = 'D:/HOMEWORK/rslab/IOCS_2019/figures/compare2/'+'i_'+str(i)+'j_'+str(j)+'_v10.png' 
            plt.show()
            plt.savefig(fname)
            plt.close('all')
def show_image(a_matrix,b_matrix,c_matrix):
    plt.matshow(c_matrix)
    plt.colorbar()
    plt.show()


## execute1
# show_image(a_200,b_200,c_200)
# plot_part(a_tc,b_tc,c_tc,img_matrix,t_matrix,t_max)
compare(a,b,c,a_ts,b_ts,c_ts,a_tc,b_tc,c_tc,a_ta,b_ta,c_ta,a_tls,b_tls,c_tls,img_matrix,t_matrix,t_max)
