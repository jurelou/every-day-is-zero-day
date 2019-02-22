#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

http://173.44.204.234:8080/
http://109.241.165.147:8080/Docsis_system.asp

"""

import os
import sys
import time
import signal
import argparse
import logging
import core.logger as log
from ipaddress import ip_address
from core.worker import Queue
from subprocess import Popen, PIPE

workers = Queue()

class ServiceExit(Exception):
	pass

def service_shutdown(signum, frame):
	logging.info('Caught signal {}'.format(signum))
	raise ServiceExit

def run_zmap(command):
	process = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	while True:
		line = process.stdout.readline().rstrip()
		if not line:
			break
		yield line

def start_scanner(plugins, max_rate, ip_range):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)
	ports = ','.join([str(port) for port,_,_ in plugins])
	command = "./masscan/bin/masscan {} -p{} --excludefile ./blacklist.txt --max-rate {}".format(ip_range, ports, max_rate)
	logging.debug("Running command: {}".format(command))
	try:
		for path in run_zmap(command):
			logging.debug("Pushing {}".format(path.decode("utf-8")))
			workers.push(path.decode("utf-8"))
		logging.info("Masscan stopped ..")
		workers.stop()
	except ServiceExit:
		logging.info("Wait, program is quitting :) .......")
		workers.stop()
		#os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def load_plugin(module):
	module_path = 'core.plugins.' + module
	if module_path in sys.modules:
		return sys.modules[module_path]
	mod =  __import__(module_path, fromlist=[module])
	plugin = mod.Plugin()
	plugin.config()
	return (plugin.port, module, plugin)

def load_plugins():
	dir = os.path.dirname(os.path.realpath(__file__))
	plugins_map = []
	for root, dirs, files in os.walk(dir + "/plugins"):  
		for filename in files:
			if filename not in ("example.py", "IPlugin.py") and filename.endswith(".py"):
				plugins_map.append(load_plugin(filename[:-3]))
	return plugins_map

def entrypoint():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--server", help="run in production mode", action="store_true")
	parser.add_argument("-d", "--dest", type=ip_address, help="Test with a given IP address")
	parser.add_argument("-p", "--plugin", type=str, help="Use a specific plugin")
	parser.add_argument('-v', '--verbose', action='count', default=0, help="Verbosity levels")
	parser.add_argument('-j', '--threads', type=int, default=1, help="Number of threads")
	parser.add_argument('-m', '--max-rate', type=int, default=150, help="maximum packets per seconds")
	parser.add_argument('-i', '--ip-range', type=str, default='0.0.0.0/0', help="IP range to scan")
	parser.add_argument('-f', '--file', action='store_true', help="Log to a file")
	args = parser.parse_args()
	threads = args.threads
	max_rate = args.max_rate
	ip_range = args.ip_range
	plugins_map = []

	if args.plugin:
		plugins_map.append(load_plugin(args.plugin))
	else:
		plugins_map = load_plugins()

	if args.server:
		threads = 100
		max_rate = 1100000
	if args.dest:
		ip_range = args.dest
	log.__setup__(args.verbose, args.file)
	log.print_config(plugins_map, args)
	workers.init(plugins_map, threads)
	start_scanner(plugins_map, max_rate, ip_range)

if __name__ == '__main__':
	if os.geteuid() != 0:
		os.execvp("sudo", ["sudo"] + sys.argv)	
	entrypoint()
