import os
import shutil
import numpy as np
from scipy.optimize import curve_fit
import spectral.io.envi as envi
from spectral import *
import cv2
import csv
    # need to find the path first
    # locate the target folder 
#### find the number of row and colume
init_state = envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/0804_0807_mean.hdr')
init_state = init_state.load()
init_state = init_state.read_band(0)
row = init_state.shape[0]
col = init_state.shape[1]
SSmax= envi.open('D:/HOMEWORK/rslab/IOCS_2019/code/New_range/ss_max_mask.hdr')
SSmax = SSmax.load()
SSmax = SSmax.read_bands(range(0,SSmax.shape[2]))

SSa = np.zeros((row, col))
SS50 = np.zeros((row, col))
SS90 = np.zeros((row, col))

for i in range(row):
    for j in range(col):
       SSa[i][j] = SSmax[i][j] - init_state[i][j]

for i in range(row):
    for j in range(col):
       SS50[i][j] = SSmax[i][j] - 0.5*SSa[i][j]
       SS90[i][j] = SSmax[i][j] - 0.9*SSa[i][j]

envi.save_image('SSa.hdr', SSa)
envi.save_image('SS50.hdr', SS50)
envi.save_image('SS90.hdr', SS90)
