# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 23:20:51 2019

@author: marti
"""

# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from NilsPodLib import session as sensor
from NilsPodLib import dataset as ds
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from scipy import signal
import datetime

plt.close('all')
#%%
file_path = r"C:\Users\marti\Google Drive\01_data_IMUandVIDEO\raw_noSync_noCalib\Team_NilsMartinTobi\Saturday_morning\3F7F\preprocessed\NilsPodX-3F7F_20190406_1036_calib_sync.csv"
#file_path = r"C:\Users\marti\Google Drive\01_data_IMUandVIDEO\raw_noSync_noCalib\Team_NilsMartinTobi\Saturday_morning\5CF4\preprocessed\NilsPodX-5CF4_20190406_1036_calib_sync.csv"
#file_path = r"C:\Users\marti\Google Drive\01_data_IMUandVIDEO\raw_noSync_noCalib\Team_NilsMartinTobi\Saturday_morning\5CF4\BackupCSV\NilsPodX-5CF4_20190406_0842_calib.csv"
#file_path = r"C:/Users/marti/Google Drive/01_data_IMUandVIDEO/raw_noSync_noCalib/Team_NilsMartinTobi/Saturday_afternoon/5CF4/NilsPodX-5CF4_20190406_1352_calib.csv"
#file_path = r"C:\Users\marti\Google Drive\01_data_IMUandVIDEO\raw_noSync_noCalib\Team_NilsMartinTobi\Friday_afternoon\5CF4\NilsPodX-5CF4_20190405_1344.csv"
#file_path = r"C:\Users\marti\Google Drive\01_data_IMUandVIDEO\raw_noSync_noCalib\Team_NilsMartinTobi\Friday_afternoon\3F7F\NilsPodX-3F7F_20190405_1346.csv"
dataset = pd.read_csv(file_path)
#%%
n = len(dataset["sample_ctr"])
sampling_rate = 204.8
start_time = 0
stop_time = n / sampling_rate
time_axis = np.arange(start_time,stop_time,1/sampling_rate)
#%%
today = datetime.datetime.now()
today_morning = datetime.datetime.strptime((today.strftime('%Y%m%d') + "000000"),"%Y%m%d%H%M%S")
session_start_time = datetime.datetime.strptime(dataset["time_received_debug"][0],"%H:%M:%S").time()
session_start_datetime = datetime.datetime.combine(today_morning.date(),session_start_time)
time_axis = [session_start_datetime+datetime.timedelta(milliseconds=idx*(1/sampling_rate)*1000) for idx,cnt in enumerate(dataset["sample_ctr"])]
#%%
plt.figure()
#plt.plot(time_axis,dataset["acc_x"],label="x")
plt.plot(time_axis,dataset["acc_y"],label="y")
#plt.plot(time_axis,dataset["acc_z"],label="z")
plt.title('Accelerometer')
plt.legend()
#%%
fc = 0.25  # Cut-off frequency of the filter
w = fc / (sampling_rate / 2) # Normalize the frequency
b, a = signal.butter(5, w, 'low')
acc_x_filtered = signal.filtfilt(b, a, dataset["acc_x"])
acc_y_filtered = signal.filtfilt(b, a, dataset["acc_y"])
acc_z_filtered = signal.filtfilt(b, a, dataset["acc_z"])
gyro_x_filtered = signal.filtfilt(b, a, dataset["gyro_x"])
gyro_y_filtered = signal.filtfilt(b, a, dataset["gyro_y"])
gyro_z_filtered = signal.filtfilt(b, a, dataset["gyro_z"])

acc_x_filtered = signal.savgol_filter(dataset["acc_x"],1201,3)
acc_x_rolling = pd.DataFrame(acc_x_filtered).rolling(2000).mean()
acc_x_sign = np.sign(acc_x_rolling)
acc_x_sign_filtered = pd.DataFrame(acc_x_sign).rolling(1000).median()
#%%
plt.figure()
plt.plot(time_axis,dataset["acc_y"],label="x_filtered")
plt.plot(time_axis,acc_x_filtered,label="x_filtered")
plt.plot(time_axis,acc_x_rolling,label="x_rolling")
plt.plot(time_axis,acc_x_sign_filtered*50,label="x_rolling_sign")
plt.hlines(0,time_axis[0],time_axis[-1])
plt.legend()
#axes[1].plot(time_axis,gyro_z_filtered,label="z")
#axes[1].plot(time_axis,gyro_x_filtered,label="z")
#axes[1].legend()
#%%
plt.figure()
#plt.plot(time_axis,acc_x_filtered,label="x")
plt.plot(time_axis,dataset["acc_y"],label="y")
#plt.plot(time_axis,acc_z_filtered,label="z")
plt.title('Accelerometer')
plt.legend()
#%%
plt.figure()
plt.plot(dataset.gyro.data)
plt.title('Gyroscope')
