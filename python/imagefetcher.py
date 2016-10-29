from multiprocessing import Queue,Process,Event
import os
from fetcher import FetcherProcess



'''
fetches the name of the most recently added image
'''
class ImageFetcher(FetcherProcess):

    # image_directory: str, absolute pathname (i.e. /home/lie/Desktop)
    # prefix: str, name of image up to number (i.e. capt)
    #dir_info = (image_directory,prefix)
    #delay: float, how long to wait to fetch next pic
    # queue: multiprocessing.Queue, shared queue for images
    def __init__(self,delay,queue,dir_info):
        image_directory,prefix = dir_info
        #the directory where images are stored
        self.image_directory = image_directory
        #the preix
        of each image file
        self.image_prefix = prefix
        #the index of the current image
        self.current_image = -1
        
        super(FetcherProcess,self).__init__(delay,queue)


   
    #fetches the next available image and attaches telemetry
    def preFetch(self):
        self.current_image+=1
        image = self.image_directory+'/'+self.image_prefix+str(self.current_image)
        file_image = None
        with open(image,'r') as file_obj:
            file_image = file_obj.read()
            self.queue.put((self.current_image,file_image))
        raise Exception('failed to read image')
    

   
