#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

"""

http://173.44.204.234:8080/
http://109.241.165.147:8080/Docsis_system.asp

"""

import sys
import time
import signal
from worker import Queue
from xml.etree.cElementTree import iterparse
import masscan2

NB_ITER = 0
MAX_ITER = 300
workers = Queue()

class ServiceExit(Exception):
	pass

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

def parse_xml(elem):
	if elem.tag == 'host':
		global NB_ITER
		NB_ITER = NB_ITER + 1
		addr = elem.getchildren()[0].get('addr')
		workers.push(addr)	

def loop(file):
	try:
		[parse_xml(elem) for event, elem in iterparse(file)]
	except Exception as e: print ('XML Error {}'.format(e))		

def main(file, plugin='livebox-20377'):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)
	workers.init(plugin)
	try:
		loop(file)
		while True:
			time.sleep(0.5)
	except ServiceExit:
		print("Service exit")
		workers.stop()

def single_test(file, addr, plugin):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)
	workers.init(plugin)
	workers.push(addr)
	workers.stop()

if __name__ == '__main__':
	mas = masscan2.PortScanner()
	mas.scan('51.38.179.48', ports='22')
	print (mas.scan_result)
	'''
	if len(sys.argv) is 2:
		main("scan.xml", sys.argv[1])
	elif len(sys.argv) is 3:
		single_test("scan.xml", sys.argv[2], sys.argv[1])
	else:
		main("scan.xml")
	'''