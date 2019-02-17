#!/usr/bin/env python3.5

import queue
import threading
import time

class Worker(threading.Thread): 
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.q = queue

	def run(self):
		print('Thread @%s started' % self.ident)
 
		while not self.shutdown_flag.is_set():
			item = self.q.get()
			print("Working on", item)
			self.q.task_done()
		print('Thread @%s stopped' % self.ident)
 

class Queue():
	def __init__(self, max_workers):
		self.max_workers = max_workers
		self.q = queue.Queue()
		self.threads = []
		for i in range(max_workers):
			t = Worker(self.q)
			t.start()
			self.threads.append(t)

	def push(self, data):
		self.q.put(data)

	def stop(self):
		for t in self.threads:
			t.shutdown_flag.set()
		for w in self.threads:
			w.join()

if __name__ == '__main__':
	pass