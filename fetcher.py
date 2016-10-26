
from multiprocessing import Process,Queue

'''
process that allows for teardown
'''
class FetcherProcess(Process):

    def __init__(self,delay,queue):
        super(Process,self).__init__()
        self.exit = multiprocessing.Event()

        self.prefetch_queue = queue 
        self.prefetch_delay = delay 
        self.prefetch_max = 0

    #size: int
    #returns the queue window size [how much can be pre-fethed]
    def setQueueWindowSize(self,size):
        self.prefeth_max = size

    #returns multiprocessing.Queue, prefetch queue 
    def getQueue(self):
        return self.Queue
    
    #dequeue special objects from queue
    def deQueue(self):
        return self.queue.get()
   
    #performs the actual prefetching option, implementation specific
    def preFetch(self):
        pass

    #overrides Process super class run
    #continues to prefetch while it can
    def run(self):
        while not self.exit.is_set():
           # if self.queue.size() < self.prefetch_max
            self.preFetch()
            sleep(self.prefetch_delay)

    #tell the process to die
    def terminate(self):
        self.exit.set()

         

