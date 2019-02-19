#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

"""

http://173.44.204.234:8080/
http://109.241.165.147:8080/Docsis_system.asp

"""

import os
import sys
import time
import signal
import core.logger as log
from core.worker import Queue
from subprocess import Popen, PIPE
from xml.etree.cElementTree import iterparse

workers = Queue()

class ServiceExit(Exception):
	pass

def service_shutdown(signum, frame):
    log.debug('Caught signal {}'.format(signum))
    raise ServiceExit

def print_config(plugin, plugin_name):
	log.debug("######## Using the following config ########")
	log.debug("Plugin:\t\t{}".format(plugin_name))
	log.debug("Nb of workers:\t{}".format(plugin.max_workers))
	log.debug("Ip range:\t{}:{}".format(plugin.ip_range, plugin.port))
	log.debug("Transmit rate:\t{}".format(plugin.max_rate))
	log.debug("Relative urls:\t{}".format(plugin.relative_url))
	log.debug("Allow redirects:\t{}".format(plugin.allow_redirects))
	log.debug("Verify ssl:\t{}".format(plugin.verify_ssl))
	log.debug("#############################################")

def run_zmap(command):
	process = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	while True:
		line = process.stdout.readline().rstrip()
		if not line:
			break
		yield line

def main(plugin_name='livebox-20377'):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)
	mod = load_plugin(plugin_name)
	plugin = mod.Plugin()
	plugin.config()
	print_config(plugin, plugin_name)
	workers.init(plugin)
	command = "./masscan/bin/masscan {} -p{} --excludefile ./blacklist.txt --max-rate {}".format(plugin.ip_range, plugin.port, plugin.max_rate)
	try:
		for path in run_zmap(command):
			log.debug("Pushing {}".format(path.decode("utf-8")))
			workers.push(path.decode("utf-8"))
		while True:
			time.sleep(1)
	except ServiceExit:
		log.err("Service exit exception")
		workers.stop()
		#os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def single_test(addr, plugin_name):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)
	mod = load_plugin(plugin_name)
	plugin = mod.Plugin()
	plugin.config()
	print_config(plugin, plugin_name)
	workers.init(plugin)
	log.debug("Running single test to {} with plugin {}".format(addr, plugin_name))
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
		main(sys.argv[1])
	elif len(sys.argv) is 3:
		single_test(sys.argv[2], sys.argv[1])
	else:
		main()
