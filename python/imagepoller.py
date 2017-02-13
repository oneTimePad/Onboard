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
	def __init__(self, next_image_number, image_poll_directory, telemetry_poll_directory,image_prefix,image_buffer):
		self.next_image_number = next_image_number
		self.image_poll_directory = image_poll_directory
		self.telemetry_poll_directory = telemetry_poll_directory
		self.next_image_filepath = self.image_poll_directory +image_prefix + str(self.next_image_number) + ".jpeg"
		self.next_telemetry_filepath = self.telemetry_poll_directory + image_prefix + str(self.next_image_number) + ".telem"
		self.image_prefix = image_prefix
		self.image_buffer = image_buffer

	# returns True if the next image is ready to be posted, returns False otherwise
	def next_image_isready(self):
		#print "POLLING FOR : " +self.next_image_filepath
		#print os.path.isfile(self.next_image_filepath)
		for rate,img in self.image_buffer:
			if os.path.isfile(self.next_image_filepath)==False:
				print "DEBUG: images not ready"
				yield rate,0
			statinfo = os.stat(self.next_image_filepath)
			#print statinfo.st_size
			#if statinfo.st_size <500000:
			#	print "DEBUG: SMALL IMAGE"

			print "DEBUG: current rate consumer: ", str(rate)
			yield rate,img

	# exposes next_image_number
	def get_next_image_number(self):
		return self.next_image_number

	# exposes next_image_filepath
	def get_next_image_filepath(self):
		return self.next_image_filepath

	# exposes next_telemetry_filepath
	def get_next_telemetry_filepath(self):
		return self.next_telemetry_filepath

	# incrememnts next_image_number and recomputes next_image_filepath
	def increment(self):
		self.next_image_number += 1
		self.next_image_filepath = self.image_poll_directory + self.image_prefix+ str(self.next_image_number) + ".jpeg"
		#print self.next_image_filepath
		self.next_telemetry_filepath = self.telemetry_poll_directory + self.image_prefix + str(self.next_image_number) + ".telem"
