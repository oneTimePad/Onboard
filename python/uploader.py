

from droneapi import DroneAPI
import time
import subprocess
import datetime
import multiprocessing
import json


def run_uploader(server_ip, server_port, username, password, next_image_number, image_poll_directory, telemetry_poll_directory, image_poll_sleep_time, trigger_start):
	#login to the ground station
	server_url = "http://"+server_ip+":"+server_port
	drone_api = DroneAPI(server_url, username, password)
	logged_in = False
	while (logged_in == False):
		try:
			drone_api.postAccess()
			logged_in = True
		except TypeError:
			print("Received incorrect padding, trying to log in again")
	print("Successfully logged in to " + server_url + " at " + str(datetime.datetime.now().time()))


	#post heartbeats and respond accordingly to the "trigger signal" or "stop triggering" signal
	currently_triggering = False
	poster = None
	while(True):
		time1 = datetime.datetime.now().time()
		heartbeat_response = drone_api.postHeartbeat()  					#post the heartbeat
		time2 = datetime.datetime.now().time()
		print("Posted heartbeat at " + str(time1) + ", received response at " + str(time2) + ", response code was " + str(heartbeat_response.status_code))
		if currently_triggering == False:
			if json.loads(heartbeat_response.text).get("heartbeat") == 1:	#check for the "start triggering" signal
				print("Trigger signal Received!")
				poster = subprocess.Popen(["python", 
							   "imageposterprocess.py", 
							   next_image_number, 
							   image_poll_directory,
							   telemetry_poll_directory,
							   server_url, 
							   server_port,
							   username, 
							   password, 
							   drone_api.access_token.token, 
							   image_poll_sleep_time], 
							  )
				trigger_start.set()
				currently_triggering = True
		if currently_triggering == True:
			if json.loads(heartbeat_response.text).get("heartbeat") == 0:	#check for the "stop triggering" signal
				print("Stop triggering signal Received!")
				trigger_start.clear()
				poster.kill()
				currently_triggering = False
		time.sleep(5) #5 is arbitrary
			
		
			
