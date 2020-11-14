import paho.mqtt.client as mqtt
import time
import sys

status = []
connected_clients = []

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    
    # We could just make USR data available to the Flask server and simply publish to it without the callbacks. Maybe a bit of a cleaner design
    client.subscribe("P2P/users")  
    client.message_callback_add("P2P/users", users_callback)   
    client.subscribe("P2P/Message")  
    client.message_callback_add("P2P/Message", message_callback) 

def message_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    payL = str(message.payload, "utf-8")
    if(payL[1] != _username[1]):
        print(payL)

# Users topic will store the client_ids of both clients.
# Will have USR data published to it & the 'middleman' will publish LED_ON if both users are present.
def users_callback(client, userdata, message):
    # Check if the client is already connected
    print(str(message.payload, "utf-8"))
    if(str(client) in connected_clients):
        idx = connected_clients.index(str(client))
        if(int(message.payload) < 200):
            # The client is at their keyboard              
            status[idx] = 1    
        else:
            status[idx] = 0
    else:
        connected_clients.append(str(client))
        status.append(0)
        payload = str(client) + " has joined the room."
        client.publish("P2P/Message", payload)
        
def message_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    payL = str(message.payload, "utf-8")
    print(payL)
      
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
if __name__ == '__main__':      
    #Instantiate MQTT client.
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
  
    while True:
        time.sleep(1)
        print(status)
        print(connected_clients)
        if(len(status) > 1):
            if(0 not in status):
                client.publish("P2P/users", "LED_ON")
            else:
                client.publish("P2P/users", "LED_OFF")       
        
