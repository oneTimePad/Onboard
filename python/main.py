from ctypes import *
from time import sleep
import pdb
from mvcam import MachineVision,MvExposure
from telemfetcher import TelemFetcher

def  main():
	cam = MachineVision("C:\\Users\\ruautonomous\\Desktop\\Onboard\\libmvcam\\Debug\\libmvcam.dll","C:\\Users\\ruautonomous\\Desktop\\pic")
	
	cam.openCam()
	exp = MvExposure(shutter=400,gain=1.0,awop=2)
	cam.setExposure(exp)
	cam.startCam(1.0)
	telem = TelemFetcher("com3")
	image_index = 1
	while True:
		image,err = cam.getImage("capt"+str(image_index)+str(".jpeg",5000)
		telemData = telem.fetchTelem()
		print telemData
		cam.saveImage(image,100)
		sleep(1)
		image_index+=1
	cam.stopCam()
	
	
	

main()