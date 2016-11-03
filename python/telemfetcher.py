
from dronekit import connect,APIException
from time import sleep

class TelemFetcher(object):
	def __init__(self,mav_server):
		self.mav_server = mav_server 
        #starts the mav connection
		try:
			self.drone = connect(self.mav_server,wait_ready = True)
		except APIException as e:
			pass
			#raise DroneTelemException(e)

	def  fetchTelem(self):
		telem = dict()
		telem['lat'] = float(self.drone.location.global_frame.lat)
		telem['lon'] = float(self.drone.location.global_frame.lon)
		telem['alt'] = float(self.drone.location.global_frame.alt)
		telem['groundcourse'] = float(self.drone.heading)
		telem['pitch'] = float(self.drone.attitude.pitch)
		telem['yaw']   = float(self.drone.attitude.yaw)
		telem['roll']  = float(self.drone.attitude.roll)
		return telem
	
	def telem2str(self,telem):
		string = '_'
		for key in telem.keys():
			string+=key+'_'+str(telem[key])
		return string
	

