

import dronekit
import serial




class TelemFetcher(object):

    """
        Connects to Mavlink (MavProxy) server to fetch telemtry informaiton
        associated with images. Waits for msg on serial from arduino to fetch
        serial.

    """

    def __init__(self,storage_template,mav_server,arduino_msg="telemtry"):

        """
        mav_server := endpoint for mavlink device
        arduino_msg:= message that is send ordering to fetch telemtry from mav
        image_id := id to save telem files with
        storage_dir:= full/path/to/image/directory/[capt]

        """


            self.mav_server = mav_server
            self.expected_msg = arduino_msg
            self.image_id = 0
            self.storage_dir = storage_template

    def connect_mav_server(self,wait_ready = True):

        """
        opens connection to mavproxy server
        raises exception on error

        """

        try:
            self.drone = dronekit.connect(self.mav_server,wait_ready=True)
        except dronekit.APIException as e:
            raise e


    def fetch_telemtry(self,timeout):
        """
        fetch telemetry from mav and return as a dictionary
        ---will implement
        """
        pass

    def start_serial_listener(self,device_port,baud=9600,time_between_images=0.5):

        """
        open serial device connection and wait for message from the arduino
        saying to fetch. write telemtry information to file

        """

        serial_listener = serial.Serial(device_port,baud,0)

        while True:
            arduino_msg = serial_listener.read()
            if arduino_msg == self.expected_msg:
                self.image_id+=1
                telemtry = self.fetch_telemtry(time_between_images/2)
                with open("".join((storage_dir,str(self.image_id),".txt")),"w")) as f:
                          f.write(str(telemtry))
