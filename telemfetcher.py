
from dronekit import connect,APIException
from time import sleep
from fetcher import FetcherProcess
'''
creates a process that fetches telemetry for images at a given delay and queues them
'''
class TelemFetcher(FetcherProcess):

    def __init__(self,mav_server,queue,delay,telem_file):
        self.mav_server = mav_server
        print(self.mav_server)
        self.drone = None
	print(delay)    
        #starts the mav connection
        try:
            self.drone = connect(self.mav_server,wait_ready = True)
        except APIException as e:
            raise DroneTelemException(e)
        print("GG")
        self.queue = queue
        super(TelemFetcher,self).__init__(queue,delay)
                

    '''
    fetches telemtry from mavlink
    returns dictionary with: [lat,lon,alt,groundcourse,pitch,yaw,roll]
    '''
    def  preFetch(self):
        print('here')
	telem = dict()
        telem['lat'] = float(self.drone.location.global_frame.lat)
        telem['lon'] = float(self.drone.location.global_frame.lon)
        telem['alt'] = float(self.drone.location.global_frame.alt)
        telem['groundcourse'] = float(self.drone.heading)
        telem['pitch'] = float(self.drone.attitude.pitch)
        telem['yaw']   = float(self.drone.attitude.yaw)
        telem['roll']  = float(self.drone.attitude.roll)
	
        self.queue.put(telem)       

