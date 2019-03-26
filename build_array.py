# pro build_array
# 'cd D:/HOMEWORK/rslab/IOCS_2019/code'
import os
import shutil

# read envi image
import spectral.io.envi as envi
from spectral import *
    # need to find the path first
    # locate the target folder 
folder = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/decay' # 要改
date = os.listdir(folder)
# print(folder_list)
    #fist loop: enter the second folder
t = 0# set the initial time in hour
martrix_number = 0
for date in date:
    for h in range(8):# find the complete file path
        print(t)
        ss_file = folder + '/'+ date+'/' +date + '_' + str(h) + '_SS.hdr'
        print(ss_file) # prove that each file is found
        
        
        data = envi.open(ss_file)
        img = data.load()
        row = img.shape[0]
        col = img.shape[1]
        # m.append(ss)
        # m.append(t)
    
        for i in range(row):
            for j in range(col):
            
            img[i,j]
            martrix_number = martrix_number + 1
        t = t + 1 
    t = t + 16


# data = envi.open(fpath + '/20150820_0_SS.hdr') # 要改
# img = data.load()
# # view = imshow(img)
# # print(img.shape[0])
# row = img.shape[0]
# col = img.shape[1]