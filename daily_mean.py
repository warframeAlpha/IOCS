# daily_mean.py
import os
import shutil
import numpy as np
#### read envi image
import spectral.io.envi as envi
from spectral import *
    # need to find the path first
    # locate the target folder 
path = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/SS/'
date = '20150807' # change the date.
img_matrix = []

for h in range(8):
    ss_file = path+date+'/'+date+ '_' + str(h) + '_SS.hdr'
    print(ss_file)
    data = envi.open(ss_file)
    img = data.read_band(0)
    img_matrix.append(img)
row = np.shape(img_matrix)[1]
col = np.shape(img_matrix)[2]
print(row,col)
img_mean = np.zeros((row, col))
for i in range(row):
    for j in range(col):
        tmp = 0
        for h in range(8):
            tmp = tmp + img_matrix[h][i][j]
        img_mean[i][j] = tmp/8
envi.save_image('D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/'+date+'/'+date+'_mean.hdr', img_mean)