#!/usr/bin/env python3.5

import sys
import time
import queue
import urllib3
import requests
import threading
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':ADH-AES128-SHA256'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QUIT = 0xDEADBEEF

class Worker(threading.Thread): 
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.q = queue

	def run(self):
		print('Thread @%s started' % self.ident)
		while not self.shutdown_flag.is_set():
			addr = self.q.get()
			if addr is QUIT:
				break
			try:
				res = requests.get('http://' + addr + ':' + PLUGIN.port, \
					allow_redirects=PLUGIN.allow_redirects, \
					timeout=PLUGIN.timeout, \
					verify=PLUGIN.verify_ssl)
				PLUGIN.exec(res)
			except requests.exceptions.SSLError: print ('SSLError from {}'.format(addr))
			except requests.exceptions.ReadTimeout: print ('timeout from {}'.format(addr))
			except Exception as e: print ('Error {} -> {}'.format(addr, e))
			finally:
				self.q.task_done()
		#print('Thread @%s stopped' % self.ident)

def load_plugin(module):
    module_path = 'plugins.' + module
    if module_path in sys.modules:
        return sys.modules[module_path]
    return __import__(module_path, fromlist=[module])

class Queue():
	def __init__(self):
		self.max_workers = None
		self.q = queue.Queue()
		self.threads = []

	def init(self, plugin):
		mod = load_plugin(plugin)
		global PLUGIN
		PLUGIN = mod.Plugin()
		PLUGIN.config()
		self.max_workers = PLUGIN.max_workers if PLUGIN.max_workers else 5
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