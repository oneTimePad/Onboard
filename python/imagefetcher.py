from mvcam import MachineVision,MvExposure,MvCamImage
import multiprocessing
import os,sys

LIBRARY_LOCATION = "C:\\Users\\ruautonomous\\Desktop\\Onboard\\libmvcam\\Debug\\libmvcam.dll"

"""
start the machine vision camera and fetches images
"""


class ImageFetcher(object):

	def __init__(self,image_parameters,storage_dir,storage_prefix,trigger_event):

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


		self.image_id = 0
		self.mvCam = MachineVision(LIBRARY_LOCATION,storage_dir)
		self.storage_dir = storage_dir
		self.storage_prefix = storage_prefix
		self.mvCam.open_cam()
		self.mvCam.set_exposure(MvExposure(shutter=self.shutter_speed,gain=self.analog_gain,aemode=self.aemode,aeop=self.aeop))

		self.trigger_event = trigger_event
		
		
	def start_capture(self,loop,delay):
		"""
		starts up the machine vision camera capturing, fetches frames from
		camera and saves them

		"""



		if self.mvCam.start_cam(int(loop*1000000), int(delay*1000000)) != 0:
			raise Exception(self.mvCam.dvpStatus)
		print "started cam loop"
		while self.trigger_event.is_set(): #while event is set
			image,err = self.mvCam.get_image(self.frame_timeout) # get fram

			if err != 0:
				raise Exception(self.mvCam.dvpStatus)

			self.image_id +=1
			name = "".join((self.storage_dir,self.storage_prefix,str(self.image_id),".jpeg"))
			print name
			image.set_name(name)

			print("But save_image returned", self.mvCam.save_image(image,self.jpeg_quality))
		self.mvCam.stop_cam()
if __name__ == "__main__":
	#newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
	image_fetcher = ImageFetcher({"shutter_speed": 33000, "gain": 2.0, "frame_timeout": 5000, "jpeg_quality": 100, "aemode": 3, "aeop": 2}, "C:\\Users\\ruautonomous\\Desktop\\extra-onboard\\nudes\\", "capt",)
	image_fetcher.start_capture(1, 1)
	print "YAY!"