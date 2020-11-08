"""EE 250L Lab 04 Starter Code

#Robert Sutherland, Seth Krieger
#GIT: https://github.com/usc-ee250-fall2020/lab05-rob/tree/lab05/ee250/lab05
#Drive: https://drive.google.com/drive/folders/13Ljqi71uNqkf6xp1ku9zclpA9hRe3q3O?usp=sharing 

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
from pynput import keyboard

# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('~/User/Desktop/GrovePi-EE250/Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')


import grovepi
from grove_rgb_lcd import *

ultPrt = 8 # D8 is the port for ultrasonic ranger
ledPrt = 2 # D2 Status LED

count = 0
buf = [0 for i in range(48)]

grovepi.pinMode(butPrt,"INPUT")
grovepi.pinMode(ledPrt,"OUTPUT")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("P2P/Message")  
    client.message_callback_add("P2P/Message", ult_callback) 
    client.subscribe("P2P/LED")
    client.message_callback_add("P2P/LED", led_callback)

#Custom callbacks need to be structured with three args like on_message()
def led_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message
    time.sleep(.5)
    print(message.topic + " " + "\"" + 
        str(message.payload, "utf-8") + "\"")
    if str(message.payload, "utf-8")== "LED_ON":
    	grovepi.digitalWrite(ledPrt, 1) #Turn LED on
    elif str(message.payload, "utf-8")== "LED_OFF":
    	grovepi.digitalWrite(ledPrt, 0) #Turn LED off

def Message_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print(message.topic + " " + "\"" + 
        str(message.payload, "utf-8") + "\"")
    setText_norefresh(str(message.payload, "utf-8"))

    	  
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    #Message limit is 48 chars.
    if(count <= 48):
    	buf = buf.append(k)
    	count = count + 1
    #If the limit is exceeded, just push the buf to the broker
    #And Clear current buf + count
    #Or if enter is pressed.
    else if(k = '{0}'or count > 48):
    	client.publish("P2P/Message", buf)
    	count = 0
    	for i in range(48):
    		buf[i] = 0	

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    #PORT14 = 14
    #grovepi.pinMode(PORT14, "INPUT")
    setRGB(100,100,100) #bright screen
    while True:
    	lis = keyboard.Listener(on_press=on_press)
    	lis.start() # start to listen on a separate thread
        
        distance = grovepi.ultrasonicRead(ultPrt)
        if(distance < 200):
        	client.publish("P2P/LED", 'LED_ON')      	
        	client.publish("P2P/ultrasonicRanger", distance)
        	time.sleep(1)
                
        on_press(lis)

