import paho.mqtt.client as mqtt
import time
import sys

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+ str(rc))
    # Subscribe to topics of interest here
    
    client.subscribe("P2P/users")  
    client.message_callback_add("P2P/users", users_callback)   
    client.subscribe("P2P/Message")  
    client.message_callback_add("P2P/Message", message_callback) 

def message_callback(client, userdata, message):
    payL = str(message.payload, "utf-8")
    if(payL[1] != _username[1]):
        print(payL)

# Users topic will store the client_ids of both clients.
# Will have USR data published to it & the 'middleman' will publish LED_ON if both users are present.
def users_callback(client, userdata, message):
    # Packet format is 'user_id':USR_data
    payload = str(message.payload, "utf-8")
    user = payload[:payload.index(":")]
    data = float(payload[payload.index(":") + 1:]) 
    print(payload)
    
    # Check if the client is already connected   
    if(user in connected_clients):
        idx = connected_clients.index(user)
        if(data > 100 or data < 0):
            # The client is not at their keyboard              
            status[idx] = False    
        else:
            status[idx] = True
    
    else:
        connected_clients.append(user)
        status.append(True)
        
def message_callback(client, userdata, message):
    payL = str(message.payload, "utf-8")
    print(payL)
      
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
    
#List containing the status (1,0)
status = []
connected_clients = []
if __name__ == '__main__':      
    #Instantiate MQTT client.
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
  
    while True:
        has_printed = False
        while(False in status):
            if(has_printed == False):
                AFK = status.index(False)
                client.publish("P2P/Message", str(connected_clients[AFK] + " is not at their keyboard."))
                has_printed = True 
                client.publish("P2P/LED", "LED_OFF")    
        has_printed = False             
        while(status.count(True) == len(status)):
            if(has_printed == False):
                client.publish("P2P/Message", "All users are at their keyboards.")
                has_printed = True
                client.publish("P2P/LED", "LED_ON")     
        
