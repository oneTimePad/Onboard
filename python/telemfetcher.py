import pdb
import serial
import multiprocessing
import json

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
		Connects to Mavlink (MavProxy) server to fetch telemetry informaiton
		associated with images. Waits for msg on serial from arduino to fetch
		serial.

	"""

	def __init__(self,storage_dir,storage_template):

		"""
		image_id := id to save telem files with
		storage_dir:= full/path/to/image/directory/[capt]

		"""



		self.storage_template = storage_template
		"""
		telem_fetcher makes a blank file before the heartbeats so we initialized image_id = -1 so
		capt stays sychronize with photos
		"""
		self.image_id = -2
		self.storage_dir = storage_dir
		self.telem_queue = None


	def telemetry_receiver(self,telem_queue):

		"""
		polls for next telemetry from telem_queue and writes it to a file

		telem_queue:= multiprocessing.Queue where telemetry is enqueued`

		"""
		try:
			while True:
				self.image_id+=1
				with open("".join((self.storage_dir,self.storage_template+str(self.image_id)+".telem")),"w") as f:
					telem = telem_queue.get(block=True)
					telem_dict = dict()
					for name,value in zip(['lat','lon','alt','roll','pitch','yaw'],telem.split(',')):
						telem_dict[name] = value
					f.write(json.dumps(telem_dict))
		except KeyboardInterrupt:
			return

	def start_telemetry_receiver(self):

		"""
			starts up telemetry receiver process which pulls telemetry from a
			queue and writes to a file with same name as associated image with
			.telem
		"""

		self.telem_queue = multiprocessing.Queue()
		receiver = multiprocessing.Process(target =
						   self.telemetry_receiver,args=(self.telem_queue,))
		receiver.daemon  = True # don't wait for it to die
		receiver.start()
		

	def start_serial_listener(self,trigger_event,device_port,baud=9600):

		"""
		open serial device connection and waits for arduino to output telemetry.
		puts telemetry in queue to be written to file

		device_port := com [windows] or device file [linux] where arduino
		serial is located
 
		baud := serial communication rate, default is 9600

		"""
		try:
			if self.telem_queue  is None:
				raise Exception("Please call start telemetry reciever first")
			while True:
				try:
					serial_listener = serial.Serial(device_port,baud) #non-blocking read
					break
				except serial.SerialException:
					continue
				except KeyboardInterrupt:
					return

			while True:
				trigger_event.wait()
				telemetry = readline(serial_listener)
				if telemetry != "":
					print(telemetry)
					self.telem_queue.put(telemetry)
		except KeyboardInterrupt:
			return
"""
if __name__ == "__main__":


	telem_fetcher = TelemFetcher("C:\\Users\\ruautonomous\\Desktop\\Onboard\\telemfile\\", "capt")
	print "reaches here 1"
	telem_fetcher.start_telemetry_receiver()
	print "reaches here 2"
	telem_fetcher.start_serial_listener("COM10", 9600)
	print "reaches here 3"
"""
