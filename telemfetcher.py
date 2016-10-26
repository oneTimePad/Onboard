
from dronekit import connect,APIException
from time import sleep
from fetcher import FetcherProcess
'''
creates a process that fetches telemetry for images at a given delay and queues them
'''
class TelemetFetcher(FetcherProcess):

    def __init__(self,mav_server,telem_file):
        self.mav_server = mav_server
        self.drone_connection = None
    
        #starts the mav connection
        try:
            self.drone_connection = connect(self.mav_server,wait_ready = True)
        except APIException as e:
            raise DroneTelemException(e)
            

                

    '''
    fetches telemtry from mavlink
    returns dictionary with: [lat,lon,alt,groundcourse,pitch,yaw,roll]
    '''
    def  preFetch(self):
        lat = float(drone.location.global_frame.lat)
        lon = float(drone.location.global_frame.lon)
        alt = float(drone.location.global_frame.alt)
        groundcourse = float(drone.heading)
        pitch = float(drone.attitude.pitch)
        yaw   = float(drone.attitude.yaw)
        roll  = float(drone.attitude.roll) 
        telem_data = dict( (name, eval(name)) for name in ['lat','lon','alt','groundcourse','pitch','yaw','roll'])
        self.queue.put(telem_data)       

