'''
This script is the only script that the user explicitly needs to run on a fly day. 
Everything else is spawned by this file or a child of this file.
This script logs in to the ground station and waits for the ground station to send the "trigger signal."
Upon receiving the trigger signal, this script spawns imageposterprocess.py and imagetakerprocess.py.
'''

import sys
from droneapi import DroneAPI
import time
import subprocess


# read all the command line inputs
if len(sys.argv) != 7:
    print("Error - Incorrect # of command line arguments passed to imageposterprocess.py." 
          "number of arguments you passed in: " + str(len(sys.argv)-1) + ", "
          "number of arguments you need to pass in: 6")
    sys.exit(1)
server_url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
next_image_number = int(sys.argv[4])
image_poll_directory = sys.argv[5]
image_poll_sleep_time = int(sys.argv[6])


#login to the ground station
drone_api = DroneAPI(server_url, username, password)
drone_api.postAccess()


#wait for the "trigger signal"
while(True):
    if !drone_api.triggerSignalReceived():
        time.sleep(5) #5 is arbitrary
    else:
        break
        

#spawn imageposterprocess.py and imagetakerprocess.py with the correct command line inputs in new cmd windows
poster = subprocess.Popen(["python", 
                           "imageposterprocess.py", 
                           str(next_image_number), 
                           image_poll_directory, 
                           server_url, 
                           username, 
                           password, 
                           drone_api.access_token.token, 
                           image_poll_sleep_time], 
                          creationflags=subprocess.CREATE_NEW_CONSOLE)
# todo spawn imagetakerprocess.py
        
    
    
