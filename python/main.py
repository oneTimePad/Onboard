import multiprocessing
from imagefetcher import ImageFetcher
from uploader import Uploader
import time
import sys
import os
server_ip = "192.168.1.224"
server_port = "8000"
username = "drone"
password = "ruautonomous"
telem_path = "/home/ruautonomous/telemfiles/"
image_path = "/home/ruautonomous/pictures/"
com_port = "/dev/ttyACM0"
file_prefix = "capt"

server_info = {"server_ip": server_ip, "server_port": server_port, "username": username, "password": password}
dir_info = {"next_image_number": 1, "image_poll_directory": image_path, "telemetry_poll_directory": telem_path,"file_prefix":file_prefix}
delay_info = {"poll_delay": 5, "heartbeat_delay": 5}

def find_next_image_num():
	image_num = 1
	while os.path.isfile(image_path+file_prefix+str(image_num)+".jpeg"):
		image_num+=1
	print "starting at image:" + str(image_num)
	return image_num
dir_info["next_image_number"] = find_next_image_num()
if __name__ == "__main__":
	trigger_event = multiprocessing.Event()
	uploader = Uploader(server_info, dir_info, delay_info)
	uploader_proc = multiprocessing.Process(target=uploader.run_uploader, args=(trigger_event,com_port))
	uploader_proc.start()
	#telem_fetcher = TelemFetcher(telem_path, file_prefix)
	#telem_fetcher.start_telemetry_receiver()
	#telem_fetcher_process = multiprocessing.Process(target=telem_fetcher.start_serial_listener, args=(trigger_event,com_port, 9600))
	#telem_fetcher_process.daemon = True
	#telem_fetcher_process.start()
	image_fetcher = ImageFetcher({"shutter_speed": 33000, "gain":2.0,"frame_timeout": 5000, "jpeg_quality":100,"aemode": 3, "aeop": 2}, dir_info,trigger_event)
	#trigger_event.set()
	while True:
		trigger_event.wait() # image_fetcher.start_capture continues as long as the event is set
		try:
			image_fetcher.start_capture(1, 1)
		except KeyboardInterrupt:
			image_fetcher.stop_capture()
			sys.exit(0)
