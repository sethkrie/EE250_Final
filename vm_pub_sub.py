"""EE 250L Lab 04 Starter Code

#Robert Sutherland, Seth Krieger
#GIT: https://github.com/usc-ee250-fall2020/lab05-rob/tree/lab05/ee250/lab05
#Drive: https://drive.google.com/drive/folders/13Ljqi71uNqkf6xp1ku9zclpA9hRe3q3O?usp=sharing 

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
from pynput.keyboard import Listener, Key

_username = ""

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    
    #We could just make USR data available to the Flask server and simply publish to it without the callbacks. Maybe a bit of a cleaner design
    client.subscribe("P2P/Message")  
    client.message_callback_add("P2P/Message", Message_callback)
    
def Message_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    payL = str(message.payload, "utf-8")
    comp = ''
    if(payL != str(_username + ": " + comp.join(buf))):
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
        time.sleep(0.2)
        buf.clear()
    elif(k_c != ''):
        buf.append(k_c)
    elif(key == Key.backspace):
        if(len(buf) > 0):
            buf.pop()
    elif(key == Key.tab):
        lis.stop()
        client.disconnect()
        
if __name__ == '__main__':
    print("Enter your username: ")
    _username = input()
    
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    
    payload = _username + " has joined the room."
    client.publish("P2P/Message", payload)
    
    lis = Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread  

    while True:   
        client.publish("P2P/users", str(_username + ':100'))
        time.sleep(1)
        on_press(lis)
        

