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
abc_powell = gdal.Open('E:/t100/regression/coefficients_gmodel_powell.tiff')
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
day = [0,24,48,72,96,168,192,216,240,264,360,384,408,432,456,500]
date = ['0811','0812','0813','0814','no data','0819','0820','0821','0822']

def plot1(x1,y1,x2,y2):
    ss1=[]
    t1=[]
    ss2=[]
    t2=[]
    t1max_index = np.argmax(img_matrix_subset[:,x1,y1])
    t1max = t_matrix[t1max_index]  
    t2max_index = np.argmax(img_matrix_subset[:,x2,y2])
    t2max = t_matrix[t2max_index]  
    for k in range(len(img_matrix_subset[:,x1,y1])):
        if img_matrix_subset[k][x1][y1]!=0:
            ss1.append(img_matrix_subset[k][x1][y1])
            t1.append(t_matrix[k])
    for k in range(len(img_matrix_subset[:,x2,y2])):
        if img_matrix_subset[k][x2][y2]!=0:
            ss2.append(img_matrix_subset[k][x2][y2])
            t2.append(t_matrix[k])        
    threshold1 = 0.1*max_variation[x1][y1] + 0.9*init_state[x1][y1]
    threshold2 = 0.1*max_variation[x2][y2] + 0.9*init_state[x2][y2]
    x11 = np.linspace(t1max,500,num=300)
    y11 = a_powell[x1][y1]*np.exp(-b_powell[x1][y1]*(x11-t1max))+c_powell[x1][y1]
    x22 = np.linspace(t2max,500,num=300)
    y22 = a_powell[x2][y2]*np.exp(-b_powell[x2][y2]*(x22-t2max))+c_powell[x2][y2]
    plt.figure(figsize=(15,6))
    plt.scatter(t1,ss1,s = 200, label = 'location1')  
    plt.scatter(t2,ss2,s = 200, label = 'location2') 
    plt.plot(x11,y11,label ='location1',linewidth = 3)
    plt.plot(x22,y22,label ='location2',linewidth = 3)
    plt.legend(fontsize = 15)

    plt.tick_params(axis = 'both', length = 20, width = 5)
    color_switcher=0
    for d in range(len(day)-1):
        if color_switcher ==0:
            plt.axvspan(day[d],day[d+1],color = '0.5',alpha=0.3)
            color_switcher = color_switcher+1
        else:
            plt.axvspan(day[d],day[d+1],color = '0.9',alpha=0.3)
            color_switcher= color_switcher - 1     

    plt.axhline(y=threshold1, color='r', linestyle='-',label = 'SS90_1')
    plt.axhline(y=threshold2, color='c', linestyle='-',label = 'SS90_2')
    plt.legend(fontsize = 15)

    plt.yticks([0,5,10,15])
    plt.tick_params(axis = 'both', length = 20, width = 5)
    plt.ylim([0,20])
    plt.xlim([0,500])
    plt.xticks(fontsize=30)            
    plt.yticks(fontsize=30)       
    plt.show()

def plott():
    k1=0.1
    k2=(1-k1)
    day = [0,24,48,72,96,168,192,216,240,264,360,384,408,432,456,500]
    print(c_powell[425][465])
    # plot the area with problems
    for i in range(426):
        for j in range(466):
            # print(c_powell[i][j])
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
                        
                x = np.linspace(tmax,500,num=500)
                y_powell = a_powell[i][j]*np.exp(-b_powell[i][j]*(x-tmax))+c_powell[i][j]
                plt.figure(figsize=(25,10))
                plt.scatter(t,ss,s = 200)  
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
                plt.xlim([0,500])
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
### Compare
plot1(1,1,5,4)# plot1(x1,y1,x2,y2)
