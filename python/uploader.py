

from droneapi import DroneAPI
from droneapierror import DroneAPICallError
import time
import subprocess
import datetime
import multiprocessing
import json
from imageposter import ImagePoster
from telemfetcher import TelemFetcher

class Uploader():

	def __init__(self, server_info, dir_info, sleep_info):
        # this is a much better way of passing arguments ... if you ever pass
        # more  than four arguments you are passing to much. This means
        # arguments can be grouped somehow

		self.dir_info = dir_info
		self.server_info = server_info
		self.sleep_info = sleep_info



    #called by multiprocessing.Process.start

	def run_uploader(self, trigger_event,serial_port,camera_trigger_params,image_buffer):
		server_ip = self.server_info["server_ip"]
		server_port = self.server_info["server_port"]
		username = self.server_info["username"]
		password = self.server_info["password"]

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
				print("DEBUG: Received incorrect padding, trying to log in again")
			except DroneAPICallError as e:
				print e
			except KeyboardInterrupt:
				return
		print("DEBUG: Successfully logged in to " + server_url + " at " + str(datetime.datetime.now().time()))


		#post heartbeats and respond accordingly to the "trigger signal" or "stop triggering" signal
		currently_triggering = False
		poster = ImagePoster(self.dir_info, drone_api, poll_delay,image_buffer)
		poster_process = multiprocessing.Process(target=poster.startPosting, args=[trigger_event])
		poster_process.daemon = True
		poster_process.start()
		telem = TelemFetcher(self.dir_info)
		telem.start_telemetry_receiver()
		telem_process = multiprocessing.Process(target=telem.start_serial_listener,args=(trigger_event,serial_port))
		telem_process.daemon = True
		telem_process.start()
		while(True):
			time1 = datetime.datetime.now().time()
			try:
				heartbeat_response = drone_api.postHeartbeat()			#post the heartbeat
			except DroneAPICallError as e:
				print e
				time.sleep(heartbeat_delay)
				continue
			except KeyboardInterrupt:
				return
			time2 = datetime.datetime.now().time()
			print("DEBUG: Posted heartbeat at " + str(time1) + ", received response at " + str(time2) + ", response code was " + str(heartbeat_response.status_code))
			resp_json = json.loads(heartbeat_response.text)
			#print "REPONSE JSON:" + str(resp_json)
			if currently_triggering == False:
				if resp_json["heartbeat"] == "true":	#check for the "start triggering" signal
					if resp_json["fps"] is not None and resp_json["gain"] is not None:
						camera_trigger_params.put((float(resp_json["fps"]),float(resp_json["gain"])))
						trigger_event.set()
						currently_triggering = True
						#print("DEBUG: Trigger signal Received!")
			if currently_triggering == True:
				if resp_json["heartbeat"] == "false":	#check for the "stop triggering" signal
					#print("DEBUG: Stop triggering signal Received!")
					trigger_event.clear()
					currently_triggering = False
				elif "new_gain" in resp_json and float(resp_json["new_gain"]) > 0:

					#print "GOT GAIN " + str(resp_json["new_gain"])
					camera_trigger_params.put(("new_gain",float(resp_json["new_gain"])))
			time.sleep(heartbeat_delay) #5 is arbitrary

