

from droneapi import DroneAPI
from droneapierror import DroneAPICallError
import time
import subprocess
import datetime
import multiprocessing
import json
from imageposter import ImagePoster


class Uploader():

	def __init__(self, server_info, dir_info, sleep_info):
        # this is a much better way of passing arguments ... if you ever pass
        # more  than four arguments you are passing to much. This means
        # arguments can be grouped somehow

		self.dir_info = dir_info
		self.server_info = server_info
		self.sleep_info = sleep_info



    #called by multiprocessing.Process.start

	def run_uploader(self, trigger_event):
		server_ip = self.server_info["server_ip"]
		server_port = self.server_info["server_port"]
		username = self.server_info["username"]
		password = self.server_info["password"]
		next_image_number = self.dir_info["next_image_number"]
		image_poll_directory = self.dir_info["image_poll_directory"]
		telemetry_poll_directory = self.dir_info["telemetry_poll_directory"]
		poll_delay = self.sleep_info["poll_delay"]
		heartbeat_delay = self.sleep_info["heartbeat_delay"]
		
		
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
			except DroneAPICallError as e:
				print e
		print("Successfully logged in to " + server_url + " at " + str(datetime.datetime.now().time()))


		#post heartbeats and respond accordingly to the "trigger signal" or "stop triggering" signal
		currently_triggering = False
		poster = ImagePoster(self.dir_info, drone_api, poll_delay)
		poster_process = multiprocessing.Process(target=poster.startPosting, args=[trigger_event])
		poster_process.daemon = True
		poster_process.start()
		while(True):
			time1 = datetime.datetime.now().time()
			try:
				heartbeat_response = drone_api.postHeartbeat()  					#post the heartbeat
			except DroneAPICallError as e:
				print e
				time.sleep(heartbeat_delay)
				continue
			time2 = datetime.datetime.now().time()
			print("Posted heartbeat at " + str(time1) + ", received response at " + str(time2) + ", response code was " + str(heartbeat_response.status_code))
			if currently_triggering == False:
				if json.loads(heartbeat_response.text).get("heartbeat") == 1:	#check for the "start triggering" signal
					print("Trigger signal Received!") 
					trigger_event.set()
					currently_triggering = True
			if currently_triggering == True:
				if json.loads(heartbeat_response.text).get("heartbeat") == 0:	#check for the "stop triggering" signal
					print("Stop triggering signal Received!")
					trigger_event.clear()
					currently_triggering = False
			time.sleep(heartbeat_delay) #5 is arbitrary
			
		
			
