from ctypes import *
from time import sleep, time
import pdb
from mvcam import MachineVision,MvExposure,mvCamImage
from telemfetcher import TelemFetcher
from gcscommand import GCSCommand
from multiprocessing import Queue,Process, Event





if __name__ == '__main__':
	host ='127.0.0.1'
	port = 2000
	trigger_event = Event()
	trigger_queue = Queue()
	cmd = GCSCommand(host,port)
	cmd.serve(trigger_queue,trigger_event)
	cam = None
	telem = None
	trigger_event.set()

	while True:
		if trigger_event.is_set():
			if cam  == None:
				cam = MachineVision('/home/lie/auvsi/Onboard/libmvcam/libmvcam.so','/home/lie/pic')
				cam.openCam()
			if telem == None:
				pass
				#telem = TelemFetcher("127.0.0.1:14550")
			exp = MvExposure(shutter=400,gain=32.0 ,awop=2)
			cam.setExposure(exp)
			cam.startCam(1.0)
			image_index = 1
			print "starting"
			while trigger_event.is_set():
				t1 = time()
				image,err = cam.getImage(5000)
				#telemData = telem.fetchTelem()
				filename = "capt"+str(image_index)+".jpeg"#telem.telem2str(telemData)+".jpeg"
				image.setName(cam.imageStorage+"//"+filename)
				#out = dill.dumps(c_char_p(image._as_parameter_.image_buffer))
				#print image._as_parameter_.image_buffer
				image_index+=1
				print(time()-t1)
				#cam.saveImage(image,100)
			cam.stopCam()
		else:
			sleep(1)
