
from dronekit import connect,APIException
from multiprocessing import Queue,Process
from time import sleep


'''
process that allows for teardown
'''
class TelemProcess(multiprocessing.Process):

    def __init__(self,):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
   
    #run argument function forever until told to stop, at given delay
    def repeatRun(self,func,delay,*args):
        while not self.exit.is_set():
            func(*args)
            sleep(delay)

    #set the event to stop the run loop
    def stop(self):
        self.exit.set()

        

'''
creates a process that fetches telemetry for images at a given delay and queues them
'''
class DroneTelemetry:

    def __init__(self,mav_server,mav_port):
        self.mav_server = mav_server
        self.mav_port   = mav_port
        self.telem_queue = Queue()
        self.drone_connection = None
       
        #starts the mav connection
        try:
            self.drone_connection = connect(self.mav_server,wait_ready = True)
        except APIException e:
            raise DroneTelemException(e) 
        
        self.executor = None
    
    '''
    fetches telemtry from mavlink
    returns dictionary with: [lat,lon,alt,groundcourse,pitch,yaw,roll]
    '''
    def  getTelem(self):
        lat = float(drone.location.global_frame.lat)
        lon = float(drone.location.global_frame.lon)
        alt = float(drone.location.global_frame.alt)
        groundcourse = float(drone.heading)
        pitch = float(drone.attitude.pitch)
        yaw   = float(drone.attitude.yaw)
        roll  = float(drone.attitude.roll)
        return dict( (name, eval(name)) for name in ['lat','lon','alt','groundcourse','pitch','yaw','roll'])
    

    '''
    called by separate process created to fetch telem
    puts the telem in a queue
    @queue: holds telemetry associated with images taken
    '''
    def enqueueTelem(self,queue):
        telem = self.getTelem()
        queue.put(telem)

    '''
    fetches telemetry from queue
    '''
    def dequeueTelem(self):
        return self.telem_queue.get()

    '''
    creates the separate process to fetch telemetry
    startes the process
    @delay: delay between getTelem function calls
    '''
    def startFetchTelem(self,delay):
       self.executor = TelemProcess()
       self.executor.repeatRun(self.enqueueTelem,delay,(self.telem_queue,))

    '''
    kills the telemetry process
    '''
    def stopFetchTelem(self)
        self.executor.stop()
        self.executor.join()
