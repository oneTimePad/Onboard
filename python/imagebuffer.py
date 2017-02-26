import multiprocessing
import time

class ImageBuffer(object):

	"""
	The purpose of this object is to control the consumption rate of imageposter to make sure there is steady throughput to the viewer without pauses
		- calculates dynamic consumption rate based on how fast producer is putting out images
		- the object iself is an iterable
	"""


	def __init__(self,max_buffer_size=10,min_buffer_size=2,mid_buffer_size=5,num_inserts_till_cal=5):
		self.image_queue = multiprocessing.Queue()
		self.not_buffering = multiprocessing.Event()
		self.max_buffer_size = max_buffer_size # despite its name it is the minimum size the buffer should be before consumption starts
		self.min_buffer_size = min_buffer_size # despite its name this is the size at which consumption halts to allow for the queue to grow back to max_buffer_size
		self.mid_buffer_size = mid_buffer_size # this is the queue size at which the rate move from fast consumption to the slow consumption phase

		self.lock = multiprocessing.Lock() #locks are needed for a consistent view of the queue size among the producer and consumer [while the queue is process-safe, the checking the size of the of
		# queue and acting accordingly is not atomic

		self.last_insert_time = 0
		self.insert_rate = multiprocessing.Value('d',0.0)
		self.insert_since_last_cal = 0
		self.num_inserts_till_cal = num_inserts_till_cal

		self.consumption_rate = 0
	def __iter__(self):
		return self

	def insert(self,image_num):
		"""
		the producer inserts the images that have 'saved' due to the fact that saving/writing is async this doesn't mean that images have been 'saved' however, due to buffering, by the time an image
		is consumed it will likely be saved
		"""

		with self.lock: #used to remove possible race condition
			#print "DEBUG: INSERTING IMAGE INTO QUEUE"
			if self.insert_since_last_cal == 0:
				self.last_insert_time = time.time()
			self.insert_since_last_cal+=1
			if  self.insert_since_last_cal == self.num_inserts_till_cal:
				self.insert_rate.value = float(((time.time()-self.last_insert_time)/self.insert_since_last_cal))
				self.insert_since_last_cal =0
				#print "DEBUG: current rate inserting: ",str(self.insert_rate.value)
			self.image_queue.put(image_num)

			if not self.not_buffering.is_set() and self.image_queue.qsize()>= self.max_buffer_size: #wait till queue_size > = init_queue_size
				self.not_buffering.set()
				#print "DEBUG: BUFFERING DONE"

	def next(self):
		"""
			iterated over by image poller to get the next ready image
			there is a very low chance that this will ever return no image due to the flow control mechanism,
			however, it is there in case the flow control fails. As to notify the consumer to stop
		"""
		#print "DEBUG: LOOKING FOR NEXT IMAGE"
		with self.lock: #adds consistent view of the queue size
			#print "DEBUG: IMAGE QUEUE SIZE:", str(self.image_queue.qsize())
			if self.image_queue.qsize() < self.min_buffer_size: #if image queue falls below a certain len (block)
				self.not_buffering.clear()

		#print "DEBUG: WAITING FOR BUFFERING"
		self.not_buffering.wait() #buffering
		with self.lock: #consumption rate calculation is not atomic and must cause the producer to wait
			rate = self.calculate_consumption_rate(self.insert_rate.value)

			return rate,self.image_queue.get()

	def calculate_consumption_rate(self,production_rate):
		"""
			calculates the rate of consumption as a function of the production rate and current queue size
			the main mechanism of flow control
		"""
		if self.image_queue.qsize() <= self.mid_buffer_size:
			self.consumption_rate = production_rate+(self.mid_buffer_size+1-self.image_queue.qsize())*.1*production_rate
			return self.consumption_rate if self.consumption_rate>0 else production_rate
		elif self.image_queue.qsize()>= self.max_buffer_size:
			self.consumption_rate = production_rate-(self.image_queue.qsize()+1-self.max_buffer_size)*.5*production_rate
			return self.consumption_rate if self.consumption_rate>0 else production_rate
		else:
			return self.consumption_rate
