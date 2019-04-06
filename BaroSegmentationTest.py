# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from NilsPodLib import session as sensor
import tkinter as tk
from tkinter import filedialog
import numpy as np
import scipy.signal

plt.close('all')

#root = tk.Tk()
#root.withdraw()
#file_path = filedialog.askopenfilename()

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'same')
    return sma


def markArea(ax, color , values, idx):
    ax.axvspan(values[idx[0]],values[idx[1]], facecolor = color, alpha = 0.1)
    for i in range(1,len(idx)-2):
        ax.axvspan(values[idx[i]+1],values[idx[i+1]], facecolor = color, alpha = 0.1)  

#file_path = '/Users/nils/Desktop/NilsPodX-3F7F_20190405_1346.bin'
file_path = '/Users/nils/Desktop/NilsPodX-5CF4_20190405_1344.bin'

dataset = sensor.Dataset(file_path)
baro_data = dataset.baro.data #eliminate first few baro samples as they often read wrong values
baro_data[0:5] = dataset.baro.data[5]

#baro_data = baro_data - np.mean(baro_data[0:500])


f, axarr = plt.subplots(3,sharex=True)
axarr[0].plot(baro_data)
axarr[1].plot(dataset.gyro.data)
axarr[2].plot(dataset.acc.data)
f.show();


baro_smooth = scipy.signal.savgol_filter(baro_data, window_length=1201, polyorder=5)
baro_smooth_avg = movingaverage(baro_smooth,4000);

baro_grad = np.gradient(baro_smooth)   
baro_grad_smooth = movingaverage(baro_grad,5000);
baro_grad_threshold = np.std(baro_grad_smooth)/10;

ride = np.where(baro_grad_smooth > baro_grad_threshold)[0]
idx_ride = np.where(np.diff(ride) > 1)
idx_ride = np.insert(idx_ride, 0, 0, axis=1)[0]

no_ride = np.where(baro_grad_smooth < -baro_grad_threshold)[0]
idx_no_ride = np.where(np.diff(no_ride) > 1)
idx_no_ride = np.insert(idx_no_ride, 0, 0, axis=1)[0]

baro_diff = np.diff(baro_smooth, n = 1)

f, axarr = plt.subplots(2,sharex=True)
axarr[0].plot(baro_data)
axarr[0].plot(baro_smooth)

axarr[1].plot(baro_grad)
axarr[1].plot(baro_grad_smooth)

markArea(axarr[0], 'r', ride, idx_ride)
markArea(axarr[0], 'b', no_ride, idx_no_ride)
f.show();

f, axarr = plt.subplots(3,sharex=True)

axarr[0].plot(dataset.baro.data)
axarr[0].plot(baro_smooth)
axarr[1].plot(dataset.gyro.data)
axarr[2].plot(dataset.acc.data)

markArea(axarr[0], 'r', ride, idx_ride)
markArea(axarr[0], 'b', no_ride, idx_no_ride)
markArea(axarr[1], 'r', ride, idx_ride)
markArea(axarr[1], 'b', no_ride, idx_no_ride)
markArea(axarr[2], 'r', ride, idx_ride)
markArea(axarr[2], 'b', no_ride, idx_no_ride)
f.show()

