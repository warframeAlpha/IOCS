# python compare.py
#cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
#This script is designed to compare two results from different methods by plotting 2 results and original data together.
import numpy as np
import spectral.io.envi as envi
from scipy.optimize import curve_fit
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
# read_50
a_50 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a_50.hdr')
b_50 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_50.hdr')
c_50 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_50.hdr')
a_50 = a_50.load()
a_50 = a_50.read_band(0)
b_50 = b_50.load()
b_50 = b_50.read_band(0)
c_50 = c_50.load()
c_50 = c_50.read_band(0)
# read_max+1
a_200 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a_200.hdr')
b_200 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_200.hdr')
c_200 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_200.hdr')
a_200 = a_200.load()
a_200 = a_200.read_band(0)
b_200 = b_200.load()
b_200 = b_200.read_band(0)
c_200 = c_200.load()
c_200 = c_200.read_band(0)

# read 800
a_800 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a_800.hdr')
b_800 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_800.hdr')
c_800 = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_800.hdr')
a_800 = a_800.load()
a_800 = a_800.read_band(0)
b_800 = b_800.load()
b_800 = b_800.read_band(0)
c_800 = c_800.load()
c_800 = c_800.read_band(0)
 
# read final
# a_final = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/a_final.hdr')
# b_final = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/b_final.hdr')
# c_final = envi.open('D:/HOMEWORK/rslab/IOCS_2019/regression/c_final.hdr')
# a_final = a_final.load()
# a_final = a_final.read_band(0)
# b_final = b_final.load()
# b_final = b_final.read_band(0)
# c_final = c_final.load()
# c_final = c_final.read_band(0)

### read time_matrix (hours)
t_matrix = [0,1,2,3,4,5,6,7,24,25,26,27,28,29,30,31,48,49,50,51,52,53,54,55,72,73,74,75,76,77,78,79,192,193,194,195,196,197,198,199,
216,217,218,219,220,221,222,223,240,241,242,243,244,245,246,247,264,265,266,267,268,269,270,271]# create a matrix to store time series
day = [0,24,48,72,96,192,216,240,264,288]
date = ['0811','0812','0813','0814','no data','0819','0820','0821','0822']
# plot
def plot1(a_50,b_50,c_50,a_200,b_200,c_200,img_matrix,t_matrix):
    ## plot a single pixel
    plt.figure(figsize=20*10)
    plt.scatter(t_matrix,img_matrix[128][368])
    x = np.linspace(0,280,num=300)
    y1 = a_50[1][1]*np.exp(-b_50[1][1]*x)+c_50[1][1]
    y2 = a_200[1][1]*np.exp(-b_200[1][1]*x)+c_200[1][1]
    y3 = a_800[1][1]*np.exp(-b_800[1][1]*x)+c_800[1][1]
    # y4 = a_800[1][1]*np.exp(-b_800[1][1]*x)+c_final[1][1]
    plt.plot(x,y1,label ='y1' )
    plt.plot(x,y2,label ='y2')
    plt.plot(x,y3,label ='y3')
    # plt.plot(x,y4,label ='y4')
    
    plt.ylim([0,5])
    plt.legend(fontsize = 20)
    plt.show()

def plot_all(a_50,b_50,c_50,a_200,b_200,c_200,img_matrix,t_matrix):
    # plot all pixel
    x = np.linspace(0,288,num=300)
    for i in range(400,img_matrix.shape[0]):
        for j in range(0,img_matrix.shape[1]):
            ss = []
            t = []
            for k in range(len(img_matrix[i][j])):
                if img_matrix[i][j][k]!=0:
                    ss.append(img_matrix[i][j][k])
                    t.append(t_matrix[k])

            y1 = a_800[i][j]*np.exp(-b_800[i][j]*x)+c_800[i][j]

            # y3 = 10*np.exp(-b_reg4[i][j]*x)+c_reg4[i][j]
            plt.figure(figsize=(20,10))
            plt.scatter(t,ss,s = 30)
            plt.title('regression result',fontsize = 50)

            plt.plot(x,y1,label ='ss = '+str(a_50[i][j]) + '*exp(-' +str(b_50[i][j])+'*t)+'+str(c_50[i][j]))
            plt.plot([0,24],[0,0],'-b',label = '0811',linewidth=4)
            plt.plot([24,48],[0,0],'-g', label = '0812',linewidth=4)
            plt.plot([48,72],[0,0],'-r',label = '0813',linewidth=4)
            plt.plot([72,96],[0,0],color = 'C0',label = '0814',linewidth=4)
            plt.plot([192,216],[0,0],'-c',label = '0819',linewidth=4)
            plt.plot([216,240],[0,0],'-m',label = '0820',linewidth=4)
            plt.plot([240,264],[0,0],'-y',label = '0821',linewidth=4)
            plt.plot([264,288],[0,0],'-k',label = '0822',linewidth=4)
            # plt.figtext(12,-2,'0807',color = 'b')
            # plt.figtext(36,-2,'0808',color = 'g')
            # plt.figtext(60,-1,'0807',color = 'r')

            plt.ylim([0,20])
            plt.legend(fontsize = 20)
            plt.xlabel('t (hours)',fontsize = 40)
            plt.ylabel('SS concentration (g/cm^3)', fontsize = 40)
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30)
            plt.axis(tight)
            fname = 'F:/Endz_Research_data/final_0715/'+'i_'+str(i)+'j_'+str(j)+'.png' 
            plt.savefig(fname)
            plt.close('all')
def plot_part(a_50,b_50,c_50,a_200,b_200,c_200,img_matrix,t_matrix):
    # plot the area with problems
    x = np.linspace(0,288,num=300)
    for i in range(150,200):
        for j in range(180,300):
            ss = []
            t = []
            for k in range(len(img_matrix[i][j])):
                if img_matrix[i][j][k]!=0:
                    ss.append(img_matrix[i][j][k])
                    t.append(t_matrix[k])

            y1 = a_800[i][j]*np.exp(-b_800[i][j]*x)+c_800[i][j]

            # y3 = 10*np.exp(-b_reg4[i][j]*x)+c_reg4[i][j]
            plt.figure(figsize=(20,10))
            plt.scatter(t,ss,s = 200)
            plt.title('regression result',fontsize = 50)
            plt.plot(x,y1,label ='ss = '+str(a_50[i][j]) + '*exp(-' +str(b_50[i][j])+'*t)+'+str(c_50[i][j]))

            for d in day:
                plt.axvline(d)
            for l in range(len(day)-1):
                plt.text(day[l]+1,10,date[l],fontsize=30)
            plt.ylim([0,12])
            plt.legend(fontsize = 20)
            plt.xlabel('t (hours)',fontsize = 40)
            plt.ylabel('SS concentration (g/m^3)', fontsize = 40)
            plt.xticks(fontsize=30)
            plt.yticks(fontsize=30)
            # plt.axis('tight')
            fname = 'D:/HOMEWORK/rslab/IOCS_2019/出圖/rec/'+'i_'+str(i)+'j_'+str(j)+'.png' 
            plt.savefig(fname)
            plt.close('all')
def save_as_tiff(a_matrix,b_matrix,c_matrix):
    cv2.imwrite('a_tiff.tiff',a_matrix)
    cv2.imwrite('b_tiff.tiff',b_matrix)
    cv2.imwrite('c_tiff.tiff',c_matrix)
def show_image(a_matrix,b_matrix,c_matrix):
    plt.matshow(c_matrix)
    plt.colorbar()
    plt.show()


## execute1
# show_image(a_200,b_200,c_200)
plot_part(a_50,b_50,c_50,a_200,b_200,c_200,img_matrix,t_matrix)