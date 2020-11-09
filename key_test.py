import time
import sys
from pynput import keyboard

buf = []
def on_press(key):
    try: 
        k_c = key.char # single-char keys
    except: 
        k_c = ''
    
    if(key == keyboard.Key.space):
        k_c = ' '
        
    if(key == keyboard.Key.enter):       
        print(buf)
        buf.clear()
    elif(k_c != ''):
        buf.append(k_c)

    			
if __name__ == '__main__':  	
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread	   		
    while True:
        on_press(lis)
        lis.join()

