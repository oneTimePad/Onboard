from mvcam import MachineVision,MvExposure,MvStrobe,MvCamImage
import multiprocessing
import os,sys

LIBRARY_LOCATION ="../libmvcam/libmvcam.so"

"""
start the machine vision camera and fetches images
"""


class ImageFetcher(object):

	def __init__(self,image_parameters,dir_info,trigger_event):

		"""
		start the image capture process and fetches frames from camera
		image_parameters := dict({
						'shutter_speed',
						'gain' //this might be removed
						'frame_timeout' //set to something high
						'jpeg_quality'
						}
						)
		storage_dir := /path/to/image/dir/
		storage_prefix := [capt]

		don't set to daemon, call stop_capture when done

		"""
		self.shutter_speed = image_parameters["shutter_speed"]
		self.analog_gain = image_parameters["gain"]
		self.frame_timeout = image_parameters["frame_timeout"]
		self.jpeg_quality = image_parameters["jpeg_quality"]
		self.aemode = image_parameters["aemode"]
		self.aeop = image_parameters["aeop"]


		self.image_id =dir_info["next_image_number"]
		self.mvCam = MachineVision(LIBRARY_LOCATION,dir_info["image_poll_directory"])
		self.storage_dir = dir_info["image_poll_directory"]
		self.storage_prefix = dir_info["file_prefix"]
		self.mvCam.open_cam()
		self.mvCam.set_exposure(MvExposure(shutter=self.shutter_speed,gain=self.analog_gain,aemode=self.aemode,aeop=self.aeop))
		self.mvCam.set_strobe(MvStrobe(image_parameters["strobe_duration"],image_parameters["strobe_output"],image_parameters["strobe_driver"]))
		self.trigger_event = trigger_event
		
	def stop_capture(self):
		self.mvCam.stop_cam()
		self.mvCam.close_cam()
		print "closed camera"
	def start_capture(self,queue):
		"""
		starts up the machine vision camera capturing, fetches frames from
		camera and saves them

		"""
		loop,delay = queue.get(block=True)

		if self.mvCam.start_cam(int(loop*1000000), int(delay*1000000)) != 0:
			raise Exception(self.mvCam.dvpStatus)
		#print "started cam loop"
		while self.trigger_event.is_set(): #while event is set
			image,err = self.mvCam.get_image(self.frame_timeout) # get fram

			if err != 0:
				raise Exception(self.mvCam.dvpStatus)

			#self.image_id +=1
			name = "".join((self.storage_dir,self.storage_prefix,str(self.image_id),".jpeg"))
			#print name
			image.set_name(name)

			err = self.mvCam.save_image(image,self.jpeg_quality)
			#if err !=1:
			#	print "SAVE _IMAGE RETURNED", err, "for",name
			self.image_id+=1
		self.mvCam.stop_cam()
		print "stopped camera"
