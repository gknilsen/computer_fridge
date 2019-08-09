#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 14:55:56 2019

@author: gni021
"""
# Script to plot the log files
# Author: Geir K. Nilsen <geir.kjetil.nilsen@gmail.com>

import matplotlib.pyplot as plt
import csv
import numpy as np
import time


time_stamp = []
fridge_temp = []
cpu_temp = []
gpu_temp = []
cpu_util = []
gpu_util = []
fridge_hum = []

path = '/home/gni021/dev/mainframe/deep_fridge/backup/test1.csv'

with open(path,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        time_stamp.append(float(row[0]))
        fridge_temp.append(float(row[1]))
        fridge_hum.append(float(row[2]))
        cpu_temp.append(float(row[3]))
        cpu_util.append(float(row[4]))
        gpu_temp.append(float(row[5]))
        gpu_util.append(float(row[6]))


fig1 = plt.figure(1)

plt.plot(time_stamp, fridge_temp, 'b')
plt.plot(time_stamp, fridge_hum, 'c')
plt.plot(time_stamp, cpu_temp, 'r')
plt.plot(time_stamp, cpu_util, '--')
plt.plot(time_stamp, gpu_temp, 'k')
plt.plot(time_stamp, gpu_util, '--')

plt.grid()

plt.legend(['Fridge temperature (deg. C)', 'Fridge humidity (%)', 'CPU temperature (deg. C)', 'CPU utilization (%)', 'GPU temperature (deg. C)', 'GPU utilization (%)'])
plt.xlabel('Time (s)')

plt.title('Test #1')


    
