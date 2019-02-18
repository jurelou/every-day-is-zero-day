#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

"""

http://173.44.204.234:8080/
http://109.241.165.147:8080/Docsis_system.asp

"""

import os
import sys
import time
import shlex
import signal
import urllib.request
import urllib.parse

from subprocess import Popen, PIPE
from worker import Queue
from xml.etree.cElementTree import iterparse

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

def run_zmap(command):
	'''
	process = Popen(shlex.split(command), stdout=PIPE)
	while True:
		output = process.stdout.readline()
		if output == '' and process.poll() is not None:
			break
		if output:
			print (output.strip().decode("utf-8"))
			workers.push('173.44.204.234')
			sys.stdout.flush()
	rc = process.poll()
	return rc	
	'''


	process = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	while True:
		line = process.stdout.readline().rstrip()
		if not line:
			break
		yield line

def main(file, plugin_name='livebox-20377'):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)

	mod = load_plugin(plugin_name)
	plugin = mod.Plugin()
	plugin.config()

	workers.init(plugin)
	try:
		print("lol")
		'''
		run_zmap("./masscan/bin/masscan 0.0.0.0/0 -p80 --excludefile ./blacklist.txt")
		'''

		for path in run_zmap("./masscan/bin/masscan 0.0.0.0/0 -p8080 --excludefile ./blacklist.txt --max-rate 150000"):
			print("Pushing ",path.decode("utf-8"))
			workers.push(path.decode("utf-8"))

		while True:
			workers.push('173.44.204.234')
	except ServiceExit:
		print("Service exit")
		workers.stop()
		#os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def single_test(file, addr, plugin_name):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)

	mod = load_plugin(plugin_name)
	plugin = mod.Plugin()
	plugin.config()

	workers.init(plugin)
	workers.push(addr)
	#workers.stop()
	#os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def load_plugin(module):
	module_path = 'plugins.' + module
	if module_path in sys.modules:
		return sys.modules[module_path]
	return __import__(module_path, fromlist=[module])

if __name__ == '__main__':
	if os.geteuid() != 0:
		os.execvp("sudo", ["sudo"] + sys.argv)	
	if len(sys.argv) is 2:
		main("scan.xml", sys.argv[1])
	elif len(sys.argv) is 3:
		single_test("scan.xml", sys.argv[2], sys.argv[1])
	else:
		main("scan.xml")