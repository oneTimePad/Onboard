from ctypes import *
from time import sleep, time
import pdb
from mvcam import MachineVision,MvExposure,mvCamImage
from telemfetcher import TelemFetcher
from gcscommand import GCSCommand
from multiprocessing import Queue,Process, Event
from PIL import Image
import piexif
import json


if __name__ == '__main__':
	host ='127.0.0.1'
	port = 2000
	trigger_event = Event()
	trigger_queue = Queue()
	cmd = GCSCommand(host,port)
	cmd.serve(trigger_queue,trigger_event)
	cam = None
	telem = None
	while True:
		if trigger_event.is_set():
			if cam  == None:
				cam = MachineVision('C:\\Users\\ruautonomous\\Desktop\\Onboard\\libmvcam\\Debug\\libmvcam.dll','C:\\Users\\ruautonomous\\Desktop\\pic')
				cam.openCam()
			if telem == None:
				telem = TelemFetcher("com3")
			exp = MvExposure(shutter=400,gain=32.0 ,awop=2)
			cam.setExposure(exp)
			cam.startCam(2.0)
			image_index = 1
			print "starting"
			while trigger_event.is_set():
				print(time())
				image,err = cam.getImage(5000)
				telemData = telem.fetchTelem()
				filename = "capt"+str(image_index)+telem.telem2str(telemData)+".jpeg"
				image.setName(cam.imageStorage+"//"+filename)
				
				image_index+=1
				cam.saveImage(image,100)
			cam.stopCam()
		else:
			sleep(1)
