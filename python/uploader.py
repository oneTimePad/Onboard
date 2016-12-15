

from droneapi import DroneAPI
import time
import subprocess
import datetime
import multiprocessing
import json
from imageposter import ImagePoster


class Uploader(object):

    def __init(self,dir_info,server_info,next_image=1,trigger_event):
        # this is a much better way of passing arguments ... if you ever pass
        # more  than four arguments you are passing to much. This means
        # arguments can be grouped somehow
        """
        dir_info := dict({"image_dir":,
                        "telem_dir":
                            })
        server_info:=dict( {"server_ip":
                        "server_port":
                        "username":
                        "password":
                        "token": (optional)
                        })
        start_img_num := image number to start at (optional)
        sleep_time:= timeout for polling (optional)

        """
        self.next_image_number = start_img_num
        self.dir_info = dir_info
        self.server_info = server_info
        self.sleep_time = sleep_time


        image_dir = self.dir_info["image_dir"]
        telem_dir = self.dir_info["telem_dir"]

        self.image_poller = ImagePoller(self.next_image_number, self.image_poll_directory, telemetry_poll_directory)

        self.drone_api=DroneAPI("http://"+self.server_info["server_ip"]+":"+self.server_info["server_port"],self.server_info["username"],self.server_info["password"])
        if self.server_info.has_key("token"):
            #this seems unecessary...
            self.drone_api.setAccessToken(self.server_info("token")
        else:
            self.drone_api.postAccess()

    #called by multiprocessing.Process.start

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
                dir_info=dict({"image_dir":image_poll_dir,"telem_dir":telemetry_poll_directory})
                server_info = dict({"server_ip":server_url,"server_port",
                                    "username":username, "password":password})
                #TODO this spawns an image poster each time a trigger signal is
                # is recieved...what is we stop triggering and retrigger? (need
                                          # to keep state
                                        #used events to pause...  
                poster = ImagePoster(dir_info,server_info,sleep_time =
                                     image_poll_sleep_time)
                poster_process = multiprocessing.Process(poster.start,args=(,))
                poster_process.daemon = True
                poster_process.start()
				trigger_start.set()
				currently_triggering = True
		if currently_triggering == True:
			if json.loads(heartbeat_response.text).get("heartbeat") == 0:	#check for the "stop triggering" signal
				print("Stop triggering signal Received!")
				trigger_start.clear()
				#poster.kill()
				currently_triggering = False
		time.sleep(5) #5 is arbitrary
			
		
			
