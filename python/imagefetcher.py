from mvcam import MachineVision,MvExposure,MvStrobe,MvCamImage,MvAeOp
import multiprocessing
import os,sys

LIBRARY_LOCATION=os.path.dirname(os.path.abspath(__file__))+"/../libmvcam/libmvcam.so"

"""
start the machine vision camera and fetches images
"""
#This delay works fine. No need to change it to change fps, just change loop.
DEFAULT_DELAY = 10000

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
		self.frame_timeout = image_parameters["frame_timeout"]
		self.jpeg_quality = image_parameters["jpeg_quality"]
		self.aemode = image_parameters["aemode"]
		self.aeop = image_parameters["aeop"]


		self.image_id =dir_info["next_image_number"]
		self.mvCam = MachineVision(LIBRARY_LOCATION,dir_info["image_poll_directory"])
		self.storage_dir = dir_info["image_poll_directory"]
		self.storage_prefix = dir_info["file_prefix"]
		self.mvCam.open_cam()
		self.mvCam.set_strobe(MvStrobe(image_parameters["strobe_duration"],image_parameters["strobe_output"],image_parameters["strobe_driver"],image_parameters["strobe_delay"]))

		self.trigger_event = trigger_event


	def stop_capture(self):
		self.mvCam.stop_cam()
		self.mvCam.close_cam()
		print "DEBUG: closed camera"
	def start_capture(self,queue,image_buffered):
		"""
		starts up the machine vision camera capturing, fetches frames from
		camera and saves them

		"""



		fps,start_gain,mode= queue.get(block=True)
		self.mvCam.set_exposure(MvExposure(shutter=self.shutter_speed,gain=start_gain,aemode=self.aemode,aeop=self.aeop))

		if mode['type'] == "auto_exposure_continuous":
			if self.mvCam.start_ae_int(int(mode['ae_target'])) != 0:
				raise Exception(self.mvCam.dvpStatus)
		elif mode['type'] == "auto_exposure_init":
			if self.mvCam.init_exposure_calibrate(int(mode['ae_target'])):
				raise Exception(self.mvCam.dvpStatus)
		else:
			print "NORMAL MODE"
			self.mvCam.set_exposure(MvExposure(shutter=self.shutter_speed,gain=start_gain,aemode=self.aemode,aeop=MvAeOp().AE_OP_OFF))


		if self.mvCam.start_cam(int((1/fps)*1000000),DEFAULT_DELAY ) != 0:
			raise Exception(self.mvCam.dvpStatus)

		while self.trigger_event.is_set(): #while event is set

			image,err = self.mvCam.get_image(self.frame_timeout) # get frame

			if err != 0:
				raise Exception(self.mvCam.dvpStatus)

			name = "".join((self.storage_dir,self.storage_prefix,str(self.image_id),".jpeg"))

			image.set_name(name)

			err = self.mvCam.save_image(image,self.jpeg_quality)
			image_buffered.insert(self.image_id)

			self.image_id+=1
			if not queue.empty() and mode['type'] != "ae_exposure_continuous" and mode['type'] != "ae_exposure_init":
				key,value= queue.get(block=False)
				if key == "new_gain":
					#print "Setting gain to : " + str(value)
					self.mvCam.set_exposure(MvExposure(shutter=self.shutter_speed,gain=value,aemode=self.aemode,aeop=MvAeOp().AE_OP_OFF))
		if mode['type'] ==  "auto_exposure_continuous":
			self.mvCam.stop_ae_int()
		self.mvCam.stop_cam()
		print "DEBUG: stopped camera"
