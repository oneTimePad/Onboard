import multiprocessing import Queue
import glob
import os



'''
fetches the name of the most recently added image
'''
class ImageFetcher:


    def __init__(self,image_directory,prefix,queue):
        self.image_directory = image_directory
        self.image_prefix = prefix
        self.current_image = -1
        self.telem_queue = queue

    #fetches the next available image and attaches telemetry
    def fetchImage(self):
        self.current_image+=1
        image = self.image_directory+'/'+self.image_prefix+str(self.current_image)
        file_image = None
        with open(image,'r') as file_obj:
            file_image = file_obj.read()
            return (self.telem_queue.get(), open(image,'r'))
        raise Exception('failed to read image')

