
from multiprocessing import Process,Queue,Event
from time import sleep
'''
process that allows for teardown
'''
class FetcherProcess(Process):

    def __init__(self,delay,queue):
        super(FetcherProcess,self).__init__()
        self.exit = Event()

        self.prefetch_queue = queue 
        self.prefetch_delay = delay 
        self.prefetch_max = 0

    #size: int
    #returns the queue window size [how much can be pre-fethed]
    def setQueueWindowSize(self,size):
        self.prefeth_max = size

    #returns multiprocessing.Queue, prefetch queue 
    def getQueue(self):
        return self.queue
    
    #dequeue special objects from queue
    def deQueue(self):
        return self.queue.get()
   
    #performs the actual prefetching option, implementation specific
    def preFetch(self):
        pass

    #overrides Process super class run
    #continues to prefetch while it can
    def run(self):
        print("Hi")
        while not self.exit.is_set():
           # if self.queue.size() < self.prefetch_max
            self.preFetch()
            sleep(1.0)

    #tell the process to die
    def terminate(self):
        self.exit.set()

         

