from mvcam import MachineVision,MvExposure,MvCamImage
import multiprocessing

LIBRARY_LOCATION = ""

"""
start the machine vision camera and fetches images
"""



class ImageFetcher(object):

    def __init__(self,image_paramters,storage_dir,storage_prefix):

        """
        start the image capture process and fetches frames from camera
        image_parameters := dict({
                        'shutter_speed',
                        'gain' //this might be removed
                        'frame_timeout' //set to something high
                        'jpeg_quality'
                        }
                        )
        storage_dir := /path/to/image/dir/
        storage_prefix := [capt]

        don't set to daemon, call stop_capture when done

        """
        self.shutter_speed = image_paramters["shutter_speed"]
        self.analog_gain = image_paramters["gain"]
        self.frame_timeout = image_paramters["frame_timeout"]
        self.jpeg_quality = image_paramters["jpeg_quality"]


        self.image_id = 0
        self.mvCam = MachineVision(LIBRARY_LOCATION,storage_dir)
        self.mvCam.open_cam()
        self.mvCam.set_exposure(MvExposure(shutter=self.shutter_speed,gain=self.gain))


        self.kill_event = multiprocessing.Event()

    def stop_capture(self):
        """
        sets the event to kill the fetching process
        """

        self.kill_event.set()

    def start_capture(self,loop,delay):
        """
        starts up the machine vision camera capturing, fetches frames from
        camera and saves them

        """



        self.mvCam.start_cam(loop,delay)

        while not self.kill_event.is_set(): #while event is not set
            image,err = self.mvCam.get_image(self.frame_timeout) # get fram

            if err is not None:
                raise Exception(err)

            self.image_id +=1
            image.set_name("".join((self.storage_dir,self.storage_prefix,str(self.image_id))))

            self.mvCam.save_image(image,self.jpeg_quality)
        self.mvCam.stop_cam()
