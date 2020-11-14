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
ts = np.linspace(0, 10, ((1/fs) * t)

distance_window = [(1/fs) * t]
for count in distance_window:
    # Poll USR value   
    time.sleep(0.05)
    distance_window[count] = grovepi.ultrasonicRead(ultPrt)
    print(distance_window[count]))
            
# Publish user's average distance over 10 seconds sampled at 20Hz to /users
avg_distance = sum(distance_window[:]) / len(distance_window)

plt.scatter(ts, distance_window) 
plt.scatter(ts, avg_distance)
plt.show() 

