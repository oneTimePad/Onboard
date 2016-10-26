#from imagefetcher import ImageFetcher
from telemfetcher import TelemFetcher
from droneapi     import DroneAPI
from multiprocessing import Queue




def main():

        api = DroneAPI()
        api.setServer('http://172.27.127.205:2000')
        api.postAccess('drone','ruautonomous')

        print('success')

        tFetcher = TelemFetcher('/dev/ttyACM0',Queue(),float(1.0),'lol.txt')
        tFetcher.start()
        while True:
            print(tFetcher.deQueue())


main()





