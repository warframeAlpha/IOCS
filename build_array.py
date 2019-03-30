# pro build_array
# cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
import os
import shutil
import numpy as np
# read envi image
import spectral.io.envi as envi
from spectral import *
    # need to find the path first
    # locate the target folder 
folder = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/decay' # 要改
date = os.listdir(folder)
# find the number of row and colume
standard_img = envi.open('D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/SS/20150803/20150803_0_SS.hdr')
standard_load = standard_img.load()
row = standard_load.shape[0]
col = standard_load.shape[1]

    #fist loop: enter the second folder
t = 0# set the initial time in hour
t_martix = [] # create a matrix to store time series
total_image_num = len(date)*8 
img_matrix = np.zeros((total_image_num, row, col))
img_index = 0 # The depth index of image matrix

for date in date:
    for h in range(8):# find the complete file path
        print(t)
        ss_file = folder + '/'+ date+'/' +date + '_' + str(h) + '_SS.hdr'
        print(ss_file) # prove that each file is found
        
        
        data = envi.open(ss_file)
        img = data.read_band(0)
        img_matrix[img_index] = img
        t_martix.append(t) 
        img_index = img_index + 1 #換下一層
        
        # for i in range(row):
        #     for j in range(col):
        #         a =2
        #     # img[i,j]
            
        t = t + 1 
    t = t + 16


# data = envi.open(fpath + '/20150820_0_SS.hdr') # 要改
# img = data.load()
# # view = imshow(img)
# # print(img.shape[0])
# row = img.shape[0]
# col = img.shape[1]