#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import sys
import time
import queue
import requests
import threading
import core.logger as log

QUIT = 0xDEADBEEF


class Worker(threading.Thread): 
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()
		self.q = queue

	def send_requests(self, addr):
		res = None
		try:
			url = 'http://{}:{}{}'.format(addr, PLUGIN.port, PLUGIN.relative_url)
			log.debug("Sending GET to {}".format(url))
			res = requests.get(url, allow_redirects=True, \
				verify=False, timeout=10)
			log.debug("Got Response {} from GET {}".format(res.status_code, addr))
		except requests.exceptions.SSLError: log.debug('SSLError from {}'.format(addr))
		except requests.exceptions.ReadTimeout: log.debug('timeout from {}'.format(addr))
		except Exception as e: log.debug('Error {} -> {}'.format(addr, e))
		finally:
			return res
	def run(self):
		log.debug("Starting new thread")
		while not self.shutdown_flag.is_set():
			addr = self.q.get()
			if addr is QUIT:
				log.debug("Thread is stopping")
				break
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