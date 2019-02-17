#!/usr/bin/env python3.5

import queue
import threading

QUIT = 0xD3ADB33F

class Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()			

	def run():
		pass

class Queue():
	def __init__(self, max_workers):
		self.max_workers = max_workers
		self.q = queue.Queue()
		self.threads = []
		for i in range(max_workers):
			t = threading.Thread(target=self.job)
			t.start()
			self.threads.append(t)
    	#self.q = queue.Queue()
	def push(self, data):
		self.q.put(data)

	def join(self):
		self.q.join()

	def job(self):
		while True:
			item = self.q.get()
			if item is QUIT:
				print ("QUIT thread")
				break
			print("Working on", item)
			self.q.task_done()	

	def stop(self):
		for i in range(self.max_workers):
			self.q.put(QUIT)
		for t in self.threads:
			t.join()

if __name__ == '__main__':
	pass