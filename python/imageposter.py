'''
This file is the main process that is responsible for polling for new images&telemetry and posting them when they become available.
This file uses an ImagePoller object to poll and a DroneAPI object to send the http post request
'''

import sys
from imagepoller import ImagePoller
from droneapi import DroneAPI
import time
import datetime


class ImagePoster(object):

    #post images and telemtry to server that are found, initialize once


	def __init__(self, dir_info, drone_api, poll_delay):
            #TODO: pass same copy of droneapi around to all (note copy does
            # not mean they are the same and are synchronized...different
            # references
		self.dir_info = dir_info
		self.next_image_number = self.dir_info["next_image_number"]
		self.image_poll_directory = self.dir_info["image_poll_directory"]
		self.telemetry_poll_directory = self.dir_info["telemetry_poll_directory"]
		self.drone_api = drone_api
		self.poll_delay = poll_delay
		self.image_poller = ImagePoller(self.next_image_number, self.image_poll_directory, self.telemetry_poll_directory)
    #TODO called by multiprocess.Process.start
	def startPosting(self, trigger_event):
        #starts the process of polling and posting images and telemtry to server
		image_poll_directory = self.image_poll_directory
		telemetry_poll_directory = self.telemetry_poll_directory
		poll_delay = self.poll_delay
		image_poller = self.image_poller
		drone_api = self.drone_api
		
        # continuously poll and post if images and telemetry are found
		print("Polling for images in the following poll location: " + image_poll_directory)
		print("Polling for telemetry in the following poll location: " + telemetry_poll_directory)
		while (True):
			trigger_event.wait()
			time1 = datetime.datetime.now().time()
			next_image_number = image_poller.get_next_image_number()
			img_filepath = image_poller.get_next_image_filepath()
			telem_filepath = image_poller.get_next_telemetry_filepath()
			print("Polling for capt" + str(next_image_number) + ".jpeg and capt" + str(next_image_number) + ".telem at " + str(time1))
			if image_poller.next_image_isready():
				posted = False
				while (posted == False):
					try:
						imgpost_response = drone_api.postImage(img_filepath, telem_filepath)
						posted = True
					except DroneAPICallError as e:
						print e
				time2 = datetime.datetime.now().time()
				print("Posted image at " + str(time1) + ", received response at " + str(time2) + ", response code was " + str(imgpost_response.status_code))
				image_poller.increment()
			else:
				time.sleep(poll_delay)


