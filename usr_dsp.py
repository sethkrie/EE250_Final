import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi

ultPrt = 4 # D4 is the port for ultrasonic ranger
           
# Moving average of distance values from USR 
distance_window = [200]
plt.axis([0, 200, 0, 500])

for count in distance_window:
    # Poll USR value   
    time.sleep(0.05)
    distance[count] = grovepi.ultrasonicRead(ultPrt)
    plt.scatter(count, distance[count])
    plt.pause(0.05)
    
plt.show()           
# Publish user's average distance over 10 seconds sampled at 20Hz to /users
avg_distance = sum(distance_window[:]) / len(distance_window)
plt.scatter(count, avg_distance)

