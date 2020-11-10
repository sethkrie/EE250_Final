"""EE 250L Lab 04 Starter Code

#Robert Sutherland, Seth Krieger
#GIT: https://github.com/usc-ee250-fall2020/lab05-rob/tree/lab05/ee250/lab05
#Drive: https://drive.google.com/drive/folders/13Ljqi71uNqkf6xp1ku9zclpA9hRe3q3O?usp=sharing 

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
from pynput.keyboard import Listener, Key
#global releaseListening
#keepListening = True

# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('~/User/Desktop/GrovePi-EE250/Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')


#import grovepi from grove_rgb_lcd import *
_username = ""

#ultPrt = 8 # D8 is the port for ultrasonic ranger
#ledPrt = 2 # D2 Status LED

#grovepi.pinMode(butPrt,"INPUT")
#grovepi.pinMode(ledPrt,"OUTPUT")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    
    #We could just make USR data available to the Flask server and simply publish to it without the callbacks. Maybe a bit of a cleaner design
    client.subscribe("P2P/ultrasonicRanger")
    client.message_callback_add("P2P/ultrasonicRanger", ult_callback)
    client.subscribe("P2P/Message")  
    client.message_callback_add("P2P/Message", Message_callback) 
    client.subscribe("P2P/LED")
    client.message_callback_add("P2P/LED", led_callback)
    
def ult_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print(message.topic + " " + "\"" + 
        str(message.payload, "utf-8") + "\"")

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
    print(str(message.payload, "utf-8"))
    setText_norefresh(str(message.payload, "utf-8"))

    	  
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
    	
if __name__ == '__main__':
    print("Enter your username: ")
    _username = input()
    lis = Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread
    
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()   
    	
    #PORT14 = 14
    #grovepi.pinMode(PORT14, "INPUT")
    #setRGB(100,100,100) #bright screen
    while True:
    	#Keyboard Handler
        on_press(lis)
        lis.join()
        
        #Poll USR value & publish (always)
       # distance = grovepi.ultrasonicRead(ultPrt)
      #  client.publish("P2P/ultrasonicRanger", distance)
        
      #  if(distance < 200):
      #       client.publish("P2P/LED", 'LED_ON')
        time.sleep(1)
        

