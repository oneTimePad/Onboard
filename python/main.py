import multiprocessing
from imagefetcher import ImageFetcher
from telemfetcher import TelemFetcher
import uploader

server_address = "172.27.63.86"
server_port = "8000"
username = "drone"
password = "ruautonomous"
telem_path = "C:\\Users\\ruautonomous\\Desktop\\Onboard\\telemfile\\"
image_path = "C:\\Users\\ruautonomous\\Desktop\\Onboard\\nudes\\"
com_port = "COM10"
file_prefix = "capt"

if __name__ == "__main__":
	trigger_start_event = multiprocessing.Event()
	uploader = multiprocessing.Process(target=uploader.run_uploader, args=(server_address, server_port, username, password, '1', image_path, telem_path, '3', trigger_start_event))
	uploader.start()
	telem_fetcher = TelemFetcher(telem_path, file_prefix)
	telem_fetcher.start_telemetry_receiver()
	telem_fetcher_process = multiprocessing.Process(target=telem_fetcher.start_serial_listener, args=(com_port, 9600))
	telem_fetcher_process.daemon = True
	#telem_fetcher_process.start()
	image_fetcher = ImageFetcher({"shutter_speed": 33000, "gain": 2.0, "frame_timeout": 5000, "jpeg_quality": 100, "aemode": 3, "aeop": 2}, image_path, file_prefix,trigger_start_event)
	while True:
		trigger_start_event.wait() # image_fetcher.start_capture continues as long as the event is set
		image_fetcher.start_capture(1, 1)
	