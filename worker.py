#!/usr/bin/env python3.5

import sys
import queue
import threading
import time

QUIT = 0xDEADBEEF

class Worker(threading.Thread): 
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.q = queue

	def run(self):
		print('Thread @%s started' % self.ident)
		while not self.shutdown_flag.is_set():
			item = self.q.get()
			if item is QUIT:
				break
			print("Working on", item)
			self.q.task_done()
			PLUGIN.exec(1)
		print('Thread @%s stopped' % self.ident)

def load_plugin(module):
    module_path = 'plugins.' + module
    if module_path in sys.modules:
        return sys.modules[module_path]
    return __import__(module_path, fromlist=[module])

class Queue():
	def __init__(self, max_workers):
		self.max_workers = max_workers
		self.q = queue.Queue()
		self.threads = []

	def init(self, plugin):
		mod = load_plugin(plugin)
		global PLUGIN 
		PLUGIN = mod.Plugin()
		PLUGIN.config()
		for i in range(self.max_workers):
			t = Worker(self.q)
			t.start()
			self.threads.append(t)

	def push(self, data):
		self.q.put(data)

	def stop(self):
		for i in range(self.max_workers):
			self.q.put(QUIT)
		for t in self.threads:
			t.shutdown_flag.set()
		for w in self.threads:
			w.join()

if __name__ == '__main__':
	pass