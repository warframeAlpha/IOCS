# test_function.py
# cd 'D:/HOMEWORK/rslab/IOCS_2019/code'
import spectral.io.envi as envi
import numpy as np
from spectral import *
def find_image_shape():
    fpath = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/SS/20150811/20150811_0_SS.hdr'# 隨便找個檔案找row/col
    r = envi.open(fpath)
    standard = r.load()
    return standard.shape
shape = find_image_shape()
row = shape[0]
col = shape[1]
m = np.zeros((3,row,col))
m2 = np.array

fpath = 'D:/HOMEWORK/rslab/IOCS_2019/ENVI_daily_data/SS/20150811/20150811_0_SS.hdr'# 隨便找個檔案找row/col
r = envi.open(fpath)
standard = r.read_band(0)
m[0] = standard
print(m[0][0][0])
print(m[0][0][1])