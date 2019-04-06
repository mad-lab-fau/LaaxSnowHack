#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 17:26:54 2019

@author: nils
"""

import matplotlib.pyplot as plt
from NilsPodLib import session as sensor
import tkinter as tk
from tkinter import filedialog
import numpy as np
import scipy.signal
import pandas as pd

path = '/Users/nils/Desktop/LAAX_Data/NilsPodX-3F7F_20190406_1036.csv'
df = pd.read_csv(path)

f, axarr = plt.subplots(3,sharex=True)

axarr[0].plot(df['baro'].values)
axarr[1].plot(df['acc_x'].values)
axarr[1].plot(df['acc_y'].values)
axarr[1].plot(df['acc_z'].values)
axarr[2].plot(df['gyro_x'].values)
axarr[2].plot(df['gyro_y'].values)
axarr[2].plot(df['gyro_z'].values)

