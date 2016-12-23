import multiprocessing
from imagefetcher import ImageFetcher
from telemfetcher import TelemFetcher
from uploader import Uploader
import time

server_ip = "172.27.63.86"
server_port = "8000"
username = "drone"
password = "ruautonomous"
telem_path = "/home/ruautonomous/telemfiles"
image_path = "/home/ruautonomous/pictures"
com_port = "/dev/ttyACM0"
file_prefix = "capt"

server_info = {"server_ip": server_ip, "server_port": server_port, "username": username, "password": password}
dir_info = {"next_image_number": 1, "image_poll_directory": image_path, "telemetry_poll_directory": telem_path}
delay_info = {"poll_delay": 5, "heartbeat_delay": 5}

if __name__ == "__main__":
	trigger_event = multiprocessing.Event()
	uploader = Uploader(server_info, dir_info, delay_info)
	uploader_proc = multiprocessing.Process(target=uploader.run_uploader, args=(trigger_event,))
	uploader_proc.start()
	telem_fetcher = TelemFetcher(telem_path, file_prefix)
	telem_fetcher.start_telemetry_receiver()
	telem_fetcher_process = multiprocessing.Process(target=telem_fetcher.start_serial_listener, args=(trigger_event,com_port, 9600))
	#telem_fetcher_process.daemon = True
	telem_fetcher_process.start()
	image_fetcher = ImageFetcher({"shutter_speed": 33000, "gain":2.0,"frame_timeout": 5000, "jpeg_quality":100,"aemode": 3, "aeop": 2}, image_path,file_prefix,trigger_event)
	while True:
		trigger_event.wait() # image_fetcher.start_capture continues as long as the event is set
		image_fetcher.start_capture(1, 1)
	
