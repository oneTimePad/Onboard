import SocketServer
from multiprocessing import Process
import json
import socket

def receive(sock):
	done = False
	data = ''
	while not done:
		data+=sock.recv(1024)
		if data[-1:] == '\n':
			return data


def sockStart(host,port,trigger_queue,trigger_event):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host,port))
		s.listen(1)
		while True:
			(gcs, address) = s.accept()
			data = receive(gcs)
			data = data[:len(data)-1]
			data = json.loads(data)
			if data['cmd'] == 'trigger':
				trigger_queue.put(data)
				trigger_event.set()
			elif data['cmd'] == 'stop_trigger':
				trigger_event.clear()
			
class GCSCommand(object):
	def __init__(self,host,port):
		self.host = host
		self.port = port
		
	
	def serve(self,trigger_queue,trigger_event):
		self.proc = Process(target= sockStart, args=(self.host,self.port,trigger_queue,trigger_event))
		self.proc.daemon = True
		self.proc.start()
