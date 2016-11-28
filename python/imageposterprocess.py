'''
This file is the main process that is responsible for polling for new images&telemetry and posting them when they become available.
This file uses an ImagePoller object to poll and a DroneAPI object to send the http post request
'''

import sys
from imagepoller import ImagePoller
from droneapi import DroneAPI
import time

# read all the command line inputs
if len(sys.argv) != 8:
    print("Error - Incorrect # of command line arguments passed to imageposterprocess.py. "
          "number of arguments you passed in: " + str(len(sys.argv)-1) + ", "
          "number of arguments you need to pass in: 7")
    sys.exit(1)
next_image_number = int(sys.argv[1])
image_poll_directory = sys.argv[2]
server_url = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]
access_token_as_text = sys.argv[6]
sleep_time = int(sys.argv[7])


# initialize the ImagePoller and DroneAPI objects
image_poller = ImagePoller(next_image_number, image_poll_directory)
drone_api = DroneAPI(server_url, username, password)
drone_api.setAccessToken(access_token_as_text)


# continuously poll and post if images and telemetry are found
while (True):
    if image_poller.next_image_isready():
        post_success = drone_api.postImage(image_poller.get_next_image_filepath(), image_poller.get_next_telemetry_filepath())
        if post_success == True:
            print("Succesfully posted " + image_poller.get_next_image_filepath())
        else:
            print("Unsuccesfully posted " + image_poller.get_next_image_filepath())
    else:
        time.sleep(sleep_time)
