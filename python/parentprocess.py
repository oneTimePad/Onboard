'''
This script is the only script that the user explicitly needs to run on a fly day. 
Everything else is spawned by this file or a child of this file.
This script logs in to the ground station and waits for the ground station to send the "trigger signal."
Upon receiving the trigger signal, this script spawns imageposterprocess.py and imagetakerprocess.py.
Then this script continues sending heartbeats and kills imageposterprocess.py and imagetakerprocess.py
upon receiving the stop triggering signal
'''

import sys
from droneapi import DroneAPI
import time
import subprocess
import datetime


# read all the command line inputs
if len(sys.argv) != 8:
    print("Error - Incorrect number of command line arguments passed to parentprocess.py.\n" 
          "Usage: python parentprocess.py [server_ip] [server_port] [username] [password] [next_image_number] [image_poll_directory] [image_poll_sleep_time]")
    sys.exit(1)
server_ip = sys.argv[1]
server_port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
next_image_number = int(sys.argv[5])
image_poll_directory = sys.argv[6]
image_poll_sleep_time = int(sys.argv[7])




#login to the ground station
server_url = "http://"+server_ip+":"+server_port
drone_api = DroneAPI(server_url, username, password)
drone_api.postAccess()
print("Successfully logged in to " + server_url + " at " + str(datetime.datetime.now().time()))


#post heartbeats and wait for the "trigger signal"
while(True):
    time1 = datetime.datetime.now().time()
    heartbeat_response = drone_api.postHeartbeat()
    time2 = datetime.datetime.now().time()
    print("Posted heartbeat at " + str(time1) + ", received response at " + str(time2) + ", response code was " + str(heartbeat_response.status_code))
    if (heartbeat_response == 'start'):
        break
    time.sleep(5) #5 is arbitrary
        

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



# wait for the "stop triggering" signal
while(True):
    heartbeat_response = drone_api.postHeartbeat()
    if (heartbeat_response == 'stop'):
        break
    time.sleep(5) #5 is arbitrary
    
    
# kill the spawned processes
poster.kill()
        
    
    
