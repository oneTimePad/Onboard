

import dronekit
import serial
import multiprocessing


def readline(ser):

    """
    reads serial until \n is seen

    ser:= serial connection object

    """


    string = ""
    while True:
        ch = ser.read()
        if(ch == '\n' or ch == ''):
            break
        string += ch
    return string


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




        self.image_id = 0
        self.storage_dir = storage_template
        self.telem_queue = None



    def telemtry_receiver(self,telem_queue):

        """
        polls for next telemetry from telem_queue and writes it to a file

        telem_queue:= multiprocessing.Queue where telemtry is enqueued`

        """
        while True:
            self.image_id+=1
            with open("".join((storage_dir,str(self.image_id),".telem")),"w") as f:
                          f.write(str(telem_queue.get()))

    def start_telemtry_receiver(self):

        """
            starts up telemetry receiver process which pulls telemtry from a
            queue and writes to a file with same name as associated image with
            .telem
        """

        self.telem_queue = multiprocessing.Queue()
        receiver = Process(target =
                           self.telemtry_receiver,args=(self.telem_queue,))
        receiver.daemon  = True # don't wait for it to die
        receiver.start()


    def start_serial_listener(self,device_port,baud=9600):

        """
        open serial device connection and waits for arduino to output telemtry.
        puts telemtry in queue to be written to file

        device_port := com [windows] or device file [linux] where arduino
        serial is located

        baud := serial communication rate, default is 9600

        """

        if self.telem_queue  is None:
            raise Exception("Please call start telemetry reciever first")

        serial_listener = serial.Serial(device_port,baud,0) #non-blocking read

        while True:
            telemtry = serial_listener.read()
            if readline(serial_listener) != "":
                self.telem_queue.put(
                    self.fetch_telemtry())
