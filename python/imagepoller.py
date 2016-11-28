import os

'''
This class is responsible for keeping track of the filepath of the next image and telemetry to be posted to the ground station and 
whether or not they are ready to be posted
'''

class ImagePoller(object):
    
    '''
        Instance variables:
          1) next_image_number: The number of the next image to be posted. This number gets incremented every time an image is succesfully
                    posted. The default starting value is 1, but this can be overidden by specifying a different value in the constructor.
          2) image_poll_directory: The path to the directory where images will be saved. This value remains constant for the entire duration
                    of flight but may change on different days (assuming we create different directories for every fly day)
          3) next_image_filepath: the full filepath of the next image to be posted. This value changes every time an image is succesfully
                    posted. This filepath is computed by concatinating image_poll_directory, next_image_value, and some other constant literals
          4) next_telemetry_filepath: the full filepath of the next telemetry file to be posted along with the image. This value changes every
                    time an image is succesfully posted. This filepath is computed by concatinating image_poll_directory, next_image_value, 
                    and some other constant literals
    '''                
          
    # Constructor, takes next_image_number (default=1) and image_poll_directory as input
    def __init__(self, next_image_number=1, image_poll_directory):
        self.next_image_number = next_image_number
        self.image_poll_directory = image_poll_directory
        # if the image poll directory does not end in a file path seperator, append one
        if (self.image_poll_directory[-1] != '/' and self.image_poll_directory != '\\'):
            self.image_poll_directory += '/'
        self.next_image_filepath = self.image_poll_directory + "capt" + str(self.next_image_number) + ".jpeg"
        self.next_telemetry_filepath = self.image_poll_directory + "telem" + str(self.next_image_number) + ".txt"
        
        
        
    # returns True if the next image is ready to be posted, returns False otherwise
    def next_image_isready(self):
        if !os.path.isfile(self.next_image_filepath) or !os.path.isfile(self.next_telemetry_filepath):
            return False
        # if the telemetry file exists but is empty, just skip over it
        if os.path.getsize(self.next_telemetry_filepath) == 0:
            self.increment()
            return False
        return True
        
    # exposes next_image_filepath
    def get_next_image_filepath(self):
        return self.next_image_filepath
    
    # exposes next_telemetry_filepath
    def get_next_telemetry_filepath(self):
        return self.next_image_filepath
    
    # incrememnts next_image_number and recomputes next_image_filepath
    def increment(self):
        self.current_image_number += 1
        self.next_image_filepath = self.image_poll_directory + "capt" + str(self.current_image_number) + ".jpeg"
        self.next_telemetry_filepath = self.image_poll_directory + "telem" + str(self.next_image_number) + ".txt"
