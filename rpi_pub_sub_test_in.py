import paho.mqtt.client as mqtt
import time
import sys
from pynput.keyboard import Listener, Key

# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
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
    payL = str(message.payload, "utf-8")
    if(payL[1] != _username[1]):
        print(payL)
    #setText_norefresh(str(message.payload, "utf-8"))

    	  
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
    led = 1
    #setRGB(100,100,100) #bright screen
    while True:
        #Keyboard Handler
        on_press(lis)
        
        #Poll USR value & publish (always)      
        time.sleep(1)
        distance = grovepi.ultrasonicRead(ultPrt)
        #client.publish("P2P/ultrasonicRanger", distance)
             
        if(distance < 200 and led == 0):
            client.publish("P2P/LED", 'LED_ON')
            payload = _username + " is at their keyboard."
    	    client.publish("P2P/Message", payload)
        elif(distance > 200 and led == 1:
            client.publish("P2P/LED", 'LED_OFF')
            payload = _username + " is away from their keyboard."
    	    client.publish("P2P/Message", payload)
    	        	    
