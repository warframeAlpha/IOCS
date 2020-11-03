#This script is designed to compare two results from different methods by plotting 2 results and original data together.
import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
import gdal
# read results from different methods and read the original data
img_matrix_subset = gdal.Open("E:/t100/regression/img_matrix_subset.dat")
# print(img_matrix_subset.RasterXSize,img_matrix_subset.RasterYSize)
img_matrix_subset = img_matrix_subset.ReadAsArray() # shape = 96,426,466
# print(img_matrix_subset.shape)
### Read powell result
abc_powell = gdal.Open('E:/t100/regression/coefficients_gmodel_powell_part.tiff')
a_powell =abc_powell.GetRasterBand(1).ReadAsArray()
b_powell =abc_powell.GetRasterBand(2).ReadAsArray()
c_powell =abc_powell.GetRasterBand(3).ReadAsArray()
print(c_powell.shape) 
abc_powell=None
### Read scipy result

init_state = gdal.Open('E:/t100/DecayData_Chau/04_07_mean_subset.tiff')
init_state = init_state.ReadAsArray()
ss_max = gdal.Open("E:/t100/ss_max_mask.tiff")
ss_max = ss_max.ReadAsArray()
max_variation = ss_max-init_state

### read time_matrix (hours)
t_matrix = []
for i in range(19):
    for j in range(8):
        if i != 4 and i!= 5 and i!= 6 and i!=11 and i!= 12 and i!= 13 and i != 14:
            t_matrix.append(24*i+j)
# print(t_matrix)
day = [0,24,48,72,96,192,216,240,264,288]
date = ['0811','0812','0813','0814','no data','0819','0820','0821','0822']

def plot1():
    ss=[]
    tt = [] # t+tmax
    t=[]
    tmax_index = np.argmax(img_matrix_subset[:,10,20])
    tmax = t_matrix[tmax_index]  

    for k in range(len(img_matrix_subset[:,10,20])):
        if img_matrix_subset[k][i][j]!=0:
            ss.append(img_matrix_subset[k][10][20])
            t.append(t_matrix[k])
            
            tt.append(tmax+t_matrix[k])
    
    x = np.linspace(tmax,440,num=300)
    # y3 = a_scipy_subset[10][20]*np.exp(-b_scipy_subset[10][20]*x)+c_scipy_subset[10][20]
    plt.figure(figsize=(25,10))
    plt.scatter(t,ss,s = 200)  
    # plt.title('regression result',fontsize = 50)

    # plt.plot(tt,y6,label ='trf_huber',linewidth = 3)
    plt.legend(fontsize = 20)
    for pos in ['right','top']:
        plt.gca().spines[pos].set_visible(True)
    for pos in ['left','bottom']:
        plt.gca().spines[pos].set_linewidth(6)

    plt.yticks([0,5,10])
    plt.tick_params(axis = 'both', length = 20, width = 5)
    plt.ylim([0,12])
    plt.xlim([0,300])
    plt.xticks(fontsize=30)            
    plt.yticks(fontsize=30)       
    # plt.axis('tight')
    fname = 'E:/t100/regression_plot/scipy_'+'i_'+str(10)+'j_'+str(20)+'.png' 
    plt.savefig(fname)
    plt.close('all')

def plott():
    k1=0.1
    k2=(1-k1)
    day = [0,24,48,72,96,168,192,216,240,264,360,384,408,432,456,500]

    # plot the area with problems
    for i in range(426):
        for j in range(466):
            if c_powell[i][j]!=-1:
                ss = []
                t=[]
                tmax_index = np.argmax(img_matrix_subset[:,i,j])
                tmax = t_matrix[tmax_index]    
                threshold = k1*max_variation[i][j] + k2*init_state[i][j]

                for k in range(len(img_matrix_subset[:,i,j])):
                    if img_matrix_subset[k][i][j]!=0:
                        ss.append(img_matrix_subset[k][i][j])
                        t.append(t_matrix[k])
                        
       
                
                x = np.linspace(tmax,440,num=300)
                y_powell = a_powell[i][j]*np.exp(-b_powell[i][j]*(x-tmax))+c_powell[i][j]
                plt.figure(figsize=(25,10))
                plt.scatter(t,ss,s = 200)  
                # plt.plot(x,y_scipy,label ='Scipy_trf',linewidth = 3)
                plt.plot(x,y_powell,label ='LMFIT_Powell',linewidth = 3)
                plt.legend(fontsize = 20)
                color_switcher=0
                for d in range(len(day)-1):
                    if color_switcher ==0:
                        plt.axvspan(day[d],day[d+1],color = '0.5',alpha=0.3)
                        color_switcher = color_switcher+1
                    else:
                        plt.axvspan(day[d],day[d+1],color = '0.9',alpha=0.3)
                        color_switcher= color_switcher - 1     

                plt.axhline(y=threshold, color='r', linestyle='-')
                plt.yticks([0,5,10,15])
                plt.tick_params(axis = 'both', length = 20, width = 5)
                plt.ylim([0,20])
                plt.xlim([0,300])
                plt.xticks(fontsize=30)            
                plt.yticks(fontsize=30)       
                # plt.axis('tight')
                fname = 'E:/t100/regression_plot/all_fig/t100_'+'i_'+str(i)+'j_'+str(j)+'.png' 
                plt.savefig(fname)
                plt.close('all')

def show_image(a_matrix,b_matrix,c_matrix):
    plt.matshow(c_matrix)
    plt.colorbar()
    plt.show()


## execute1
# show_image(a_200,b_200,c_200)
# plott(a_scipy_subset,b_scipy_subset,c_scipy_subset,img_matrix_subset)
plott()