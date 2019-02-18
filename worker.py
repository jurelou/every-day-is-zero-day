#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import sys
import time
import queue
import requests
import threading

QUIT = 0xDEADBEEF

class Worker(threading.Thread): 
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.q = queue

	def send_requests(self, addr):
		res = None
		'''
		print ("Forge url: ", url)
		try:
			res = requests.get(url)
			print (res)
		except Exception as e: print ('Error {} -> {}'.format(addr, e))
		finally:
			return None

		'''
		try:
			url = 'http://' + addr + ':' + PLUGIN.port + PLUGIN.relative_url
			print ("Requesting", url)
			res = requests.get(url, allow_redirects=True, \
				verify=False, timeout=10)
			print ("->>>>", res)
			sys.stdout.flush()
		except requests.exceptions.SSLError: print ('SSLError from {}'.format(addr))
		except requests.exceptions.ReadTimeout: print ('timeout from {}'.format(addr))
		except Exception as e: print ('Error {} -> {}'.format(addr, e))
		finally:
			return res
	def run(self):
		print('Starting new thread')
		while not self.shutdown_flag.is_set():
			addr = self.q.get()
			if addr is QUIT:
				break
			print("GOT ", addr)
			'''
			print("Sending request")
			with urllib.request.urlopen('http://www.python.org/') as f:
				print(f.read(100))
			sys.stdout.flush			
			'''

			res = self.send_requests(addr)
			if res:
				PLUGIN.exec(res)
			self.q.task_done()

class Queue():
	def __init__(self):
		self.max_workers = None
		self.q = queue.Queue()
		self.threads = []

	def init(self, plugin):
		global PLUGIN
		PLUGIN = plugin
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