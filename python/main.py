import multiprocessing
from imagefetcher import ImageFetcher
from uploader import Uploader
from mvcam import MvAeMode,MvAeOp,MvStrobeOutput,MvStrobeDriver
from imagebuffer import ImageBuffer
import time
import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("server")
parser.add_argument("port")
parser.add_argument("pictures")
parser.add_argument("telems")
args = parser.parse_args()

server_ip = str(args.server)
server_port = str(args.port)
username = "drone"
password = "ruautonomous"
image_path = str(args.pictures) 
telem_path = str(args.telems)
com_port = "/dev/ttyACM0"
file_prefix = str(int(time.time()))+"capt" 
print image_path
print telem_path
server_info = {"server_ip": server_ip, "server_port": server_port, "username": username, "password": password}
dir_info = {"next_image_number": 1, "image_poll_directory": image_path, "telemetry_poll_directory": telem_path,"file_prefix":file_prefix}
delay_info = {"poll_delay": 2, "heartbeat_delay": 2}
cam_info={"shutter_speed":400,"gain":1.0,"frame_timeout":5000,"jpeg_quality":100,"aemode":MvAeMode().AE_MODE_AG_ONLY,"aeop":MvAeOp().AE_OP_CONTINUOUS,"strobe_delay":1000000.0,"strobe_duration":100.0,"strobe_output":MvStrobeOutput().STROBE_OUT_HIGH,"strobe_driver":MvStrobeDriver().TIMER_LOGIC}

def find_next_image_num():
	image_num = 1
	while os.path.isfile(image_path+file_prefix+str(image_num)+".jpeg"):
		image_num+=1
		print "DEBUG: starting at image:" + str(image_num)
	return image_num
dir_info["next_image_number"] = find_next_image_num()
if __name__ == "__main__":
	trigger_event = multiprocessing.Event()
	camera_trigger_params = multiprocessing.Queue()
	uploader = Uploader(server_info, dir_info, delay_info)
	#image_buffered =  multiprocessing.Event()
	image_buffer = ImageBuffer(max_buffer_size=4,mid_buffer_size=2)
	image_fetcher = ImageFetcher(cam_info, dir_info,trigger_event)

	uploader_proc = multiprocessing.Process(target=uploader.run_uploader, args=(trigger_event,com_port,camera_trigger_params,image_buffer))
	uploader_proc.start()

	while True:
		try:
			trigger_event.wait() # image_fetcher.start_capture continues as long as the event is set
			image_fetcher.start_capture(camera_trigger_params,image_buffer)
		except KeyboardInterrupt:
			print "DEBUG: CLOSING!"
			image_fetcher.stop_capture()

			sys.exit(0)
