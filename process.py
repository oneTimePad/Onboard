
import multiprocessing

'''
process that allows for teardown
'''
class EProcess(multiprocessing.Process):

    def __init__(self,):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
   
    #run argument function forever until told to stop, at given delay
    def repeatRun(self,func,delay,*args):
        while not self.exit.is_set():
            func(*args)
            sleep(delay)

    #set the event to stop the run loop
    def stop(self):
        self.exit.set()

        

