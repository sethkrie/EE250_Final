import time
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi

ultPrt = 4 # D4 is the port for ultrasonic ranger
           
# Moving average of distance values from USR 
t = 10
fs = 20
distance_window = []


for i in range(t * fs):
    # Poll USR value   
    time.sleep(0.05)
    distance_window.append(grovepi.ultrasonicRead(ultPrt))
    print(distance_window[i])
            
# Publish user's average distance over 10 seconds sampled at 20Hz to /users
avg_distance = sum(distance_window[:]) / len(distance_window)

plt.scatter(ts, distance_window) 
plt.scatter(ts, avg_distance)
plt.show() 

