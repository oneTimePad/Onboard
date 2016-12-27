import multiprocessing
import time

class ImageBuffer(object):

	def __init__(self,max_buffer_size=10,min_buffer_size=2):
		self.image_queue = multiprocessing.Queue()
		self.not_buffering = multiprocessing.Event()
		self.max_buffer_size = max_buffer_size
		self.min_buffer_size = min_buffer_size
		self.lock = multiprocessing.Lock()
		self.init_done = False

		self.last_insert_time = 0
		self.insert_rate = multiprocessing.Value('d',0.0)
		self.insert_since_last_cal = 0
		self.num_inserts_till_cal = 5
	def __iter__(self):
		return self

	def insert(self,image_num):
		with self.lock: #used to remove possible race condition
			print "PUTTING"
			if self.insert_since_last_cal == 0:
				self.last_insert_time = time.time()
			self.insert_since_last_cal+=1
			if  self.insert_since_last_cal == self.num_inserts_till_cal:
				self.insert_rate.value = float(((time.time()-self.last_insert_time)/self.insert_since_last_cal))
				self.insert_since_last_cal =0
				print "current rate inserting: ",str(self.insert_rate.value)
			self.image_queue.put(image_num)

			if not self.not_buffering.is_set() and self.image_queue.qsize()>= self.max_buffer_size: #wait till queue_size > = init_queue_size
				#self.init_done = True
				self.not_buffering.set()
				print "BUFFERING DONE"
			"""
			elif self.init_done and self.image_queue.qsize() >= self.min_buffer_size: #wait till queue_size > = min_queue_size
				self.not_buffering.set()
				print "DONE BUFFERING"

			"""
	def next(self):
	
		with self.lock: #adds consistent view of the queue size
			print self.image_queue.qsize()
			if self.image_queue.qsize() < self.min_buffer_size: #if image queue falls below a certain len (block)
				self.not_buffering.clear()
			
			
		print "WAITING"
		self.not_buffering.wait() #buffering
		with self.lock:
		#print insert_rate
			return self.insert_rate.value,self.image_queue.get()
