#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:15:42 2019

@author: gni021
"""

# Python deep fridge data logger for test #5
# Author: Geir K. Nilsen <geir.kjetil.nilsen@gmail.com>
#

import serial
import time
import subprocess
import sys
from pytictoc import TicToc

tictoc = TicToc()

dev = '/dev/ttyACM0'
baud_rate = 9600
path = '/home/gni021/deep_fridge/tests/%s' % sys.argv[1]
file = open(path,'w')

try:
    ser = serial.Serial(dev, baud_rate, timeout=10)
    print('Initializing serial connection to %s with %d bps...' % (dev, baud_rate))
    time.sleep(1)
except serial.SerialException:
    print('Could not connect to %s' % dev)
    sys.exit(-1)

print('OK')
print('Deep Fridge Logger v0.1 -- Press Ctrl-C to stop logging.')
print('Log file: %s' % path)

cmd = ''
counter = 0
time_stamp = 0.0
compressor_running = False
cpugpu_started = False

# Skip the first 3 DHT-11 readings (they tend to be outdated for some reason)
while counter < 3:
    ser.write('t'.encode())
    resp = ser.readline()
    try:
        fridge_temp = float(resp)
    except ValueError:
        continue
    
    ser.write('h'.encode())
    resp = ser.readline()
    try:
        fridge_hum = float(resp)
    except ValueError:
        continue   

    time.sleep(1)
    counter = counter + 1
    
counter = 0

# Start compressor
ser.write('1'.encode())

# Run for 60 minutes
while time_stamp < 3600:
    tictoc.tic()
    ser.write('t'.encode())
    resp = ser.readline()
    try:
        fridge_temp = float(resp)
    except ValueError:
        continue
    
    ser.write('h'.encode())
    resp = ser.readline()
    try:
        fridge_hum = float(resp)
    except ValueError:
        continue   
    
    p1 = subprocess.Popen(('sensors', 'it8665-isa-0290'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'temp3'), stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p3 = subprocess.Popen(('cut', '-c16-19'), stdin=p2.stdout, stdout=subprocess.PIPE)
    p2.stdout.close()
    cpu_temp = p3.communicate()[0].decode()
    p3.stdout.close()

    p1 = subprocess.Popen(args=('nvidia-smi', '-q', '-d', 'temperature'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'GPU Current'), stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p3 = subprocess.Popen(('cut', '-c39-40'), stdin=p2.stdout, stdout=subprocess.PIPE)
    p2.stdout.close()
    gpu_temp = p3.communicate()[0].decode()
    p3.stdout.close()
    
    p1 = subprocess.Popen(args=('nvidia-smi', '-q', '-d', 'utilization'), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(('grep', 'Gpu'), stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p3 = subprocess.Popen(('cut', '-c39-41'), stdin=p2.stdout, stdout=subprocess.PIPE)
    p2.stdout.close()
    gpu_util = p3.communicate()[0].decode()
    p3.stdout.close()
    
 
    p1 = subprocess.Popen(args=('sh', 'cpu_usage.sh'), stdout=subprocess.PIPE)
    cpu_util = p1.communicate()[0].decode()
    p1.stdout.close()
        
    
    reading = str(round(time_stamp, 1)) + ',' + str(fridge_temp) + ',' + str(fridge_hum) + ',' + \
              str(cpu_temp.strip()) + ',' + str(cpu_util.strip()) + ',' + \
              str(gpu_temp.strip()) + ',' + str(gpu_util.strip().strip('%')) + '\n'
    print(reading, end='')
    file.write(reading)
    file.flush()
    counter = counter + 1
    time_stamp = time_stamp + tictoc.tocvalue()
    
    
    # Start GPU after 45 minutes, leave it on max for 5 minutes
    if time_stamp > 2700 and cpugpu_started != True:
        p1 = subprocess.Popen(args=('./gpu_burn', '300'))
        cpugpu_started = True
    
   
# turn compressor off
ser.write('0'.encode())
file.close()
ser.close()
print('Good bye')
