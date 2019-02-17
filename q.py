
import threading

class   Worker(threading.Thread):
	def __init__(self, conn, client):
		threading.Thread.__init__(self)
		self.conn = conn
		self.client = client
		self.shutdown_flag = threading.Event()

	def run(self):
		log.info("Starting thread", self.ident)
		while not self.shutdown_flag.is_set():
			pass;
		log.info("Thread", self.ident, "stopped")

class Queue():
    def __init__(self,*args,**kwargs):
    	pass