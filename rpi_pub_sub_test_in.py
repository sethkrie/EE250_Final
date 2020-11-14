import paho.mqtt.client as mqtt
import time
import sys
import numpy
from pynput.keyboard import Listener, Key

sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi
_username = ""

ledPrt = 2 # D2 Status LED
ultPrt = 4 # D4 is the port for ultrasonic ranger
grovepi.pinMode(ledPrt,"OUTPUT")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    
    #We could just make USR data available to the Flask server and simply publish to it without the callbacks. Maybe a bit of a cleaner design
    client.subscribe("P2P/users")  
    client.message_callback_add("P2P/users", users_callback)   
    client.subscribe("P2P/Message")  
    client.message_callback_add("P2P/Message", message_callback) 

def message_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    payL = str(message.payload, "utf-8")
    if(payL[1] != _username[1]):
        print(payL)

#Users topic will store the client_ids of both clients.
#Will have USR data published to it & the 'middleman' will publish LED_ON if both users are present.
def users_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message
    if str(message.payload, "utf-8")== "LED_ON":      
        print('Both users are present.')
        grovepi.digitalWrite(ledPrt, 1) #Turn LED on
    elif str(message.payload, "utf-8")== "LED_OFF":
        grovepi.digitalWrite(ledPrt, 0) #Turn LED off

def message_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    payL = str(message.payload, "utf-8")
    if(payL[1] != _username[1]):
        print(payL)
      
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
buf = []
def on_press(key):
    try: 
        k_c = key.char # single-char keys
    except: 
        k_c = ''
    
    if(key == Key.space):
        k_c = ' '
        
 #Add conditional for length limit of message depending on LCD OR scrolling LCD output
    if(key == Key.enter):
        payload = ''
        payload = _username + ": " + payload.join(buf) 
        client.publish("P2P/Message", payload) #In MQTT, publish this buf to the broker
        buf.clear()
    elif(k_c != ''):
        buf.append(k_c)
    elif(key == Key.backspace):
        buf.pop()
    
if __name__ == '__main__':   
    print("Enter your username: ")
    _username = input()
    #Inform the middleman of who joined.  
    #client.publish("P2P/users", "U: " + _username)
    
    #Instantiate MQTT client.
    client = mqtt.Client(client_id = _username)
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()   
    
    lis = Listener(on_press=on_press)
    lis.start() # Start to listen on a separate thread  
    led = 1
           
    fs = 20  
    t = 10 
    while True:       
        # Keyboard Handler
        on_press(lis)
        
        # Moving average of distance values from USR 
        avg_distance    = []
        for i in range(t):
            # Observe a data in a window of 5 samples (1 second)
            distance_window = []
            for j in range(fs):
                # Poll USR value   
                time.sleep(0.05)
                distance_window.append(grovepi.ultrasonicRead(ultPrt))      
            avg_distance.append(numpy.cumsum(distance_window) / len(distance_window))
                     
        # We don't want excessive updates in case a user bumps the sensor.
        # Look at the averge of the moving window across 10s
        # Publish user's average distance over 10 seconds sampled at 20Hz to /users
        avg = numpy.cumsum(avg_distance) / len(distance_window)      
        client.publish("P2P/users", avg)
        avg_distance.clear()
        

