import multiprocessing import Queue
import glob
import os



'''
fetches the name of the most recently added image and queues it up
'''
class ImageFetcher:


    def __init__(self,image_directory,delay):
        self.image_directory = image_directory
        self.delay = delay
        self.image_queue = Queue() 
        self.executor = None
    
    '''
    get the name of the most recently added image to the given directory 
    '''
    def fetchImage(self,queue):
        newestImage = min(glob.iglob('*.jpeg'), key = os.path.getctime)
        queue.put(newestImage)

    '''
    return the name of the next image in the queue
    '''
    def getImage(self)
        return queue.get()

    '''
    start the fetching process
    '''
    def startFetching(self):
        self.executor = EProcess()
        self.executor.repeatRun(self.fetchImage,delay,(self.image_queue,))

    '''
    stop the fetching process
    '''
    def stopFetching(self):
        self.executor.stop()
        self.executor.join()


