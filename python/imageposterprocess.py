'''
This file is the main process that is responsible for polling for new images&telemetry and posting them when they become available.
This file uses an ImagePoller object to poll and a DroneAPI object to send the http post request
'''

import sys
from imagepoller import ImagePoller
from droneapi import DroneAPI
import time
import datetime

# read all the command line inputs
if len(sys.argv) != 9:
    print("Error - Incorrect number of command line arguments passed to imageposterprocess.py.\n" 
          "Usage: python imageposterprocess.py [next_image_number] [image_poll_directory] [server_ip] [server_port] [username] [password] [access_token_as_text] [sleep_time]")
    sys.exit(1)
next_image_number = int(sys.argv[1])
image_poll_directory = sys.argv[2]
server_ip = sys.argv[3]
server_port = sys.argv[4]
username = sys.argv[5]
password = sys.argv[6]
access_token_as_text = sys.argv[7]
sleep_time = int(sys.argv[8])


# initialize the ImagePoller and DroneAPI objects
image_poller = ImagePoller(next_image_number, image_poll_directory)
server_url = "http://"+server_ip+":"+server_port
drone_api = DroneAPI(server_url, username, password)
# if access_token_as_text is passed in as "unknown", allow the drone_api object to login. If access_token_as_text is passed in as "nologin", just leave the token as None. Otherwise, set the access token to the passed in value
if access_token_as_text == "unknown":
	drone_api.postAccess()
	print("Successfully logged in to " + server_url + " at " + str(datetime.datetime.now().time()))
elif access_token_as_text == "nologin":
	pass
else:
	drone_api.setAccessToken(access_token_as_text)


# continuously poll and post if images and telemetry are found
print("Starting to poll in the following poll location: " + image_poll_directory)
while (True):
	time1 = datetime.datetime.now().time()
	print("Polling for img+telem #" + str(image_poller.get_next_image_number()) + " at " + str(time1))
	img_filepath = image_poller.get_next_image_filepath()
	telem_filepath = image_poller.get_next_telemetry_filepath()
	if image_poller.next_image_isready():
        #imgpost_response = drone_api.postImage(img_filepath, telem_filepath)
		#print(imgpost_response.status_code)
		image_poller.increment()
	else:
		time.sleep(sleep_time)
