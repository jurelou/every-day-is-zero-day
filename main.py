#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

"""

http://173.44.204.234:8080/
http://109.241.165.147:8080/Docsis_system.asp

"""

import os
import argparse
import sys
import time
import signal
from ipaddress import ip_address
import core.logger as log
from core.worker import Queue
from subprocess import Popen, PIPE
from xml.etree.cElementTree import iterparse

workers = Queue()

class ServiceExit(Exception):
	pass

def service_shutdown(signum, frame):
    log.all('Caught signal {}'.format(signum))
    raise ServiceExit

def print_config(plugin, args):
	log.all("######## Using the following config ########")
	log.all("Plugin:\t\t{}".format(args.plugin))
	log.all("Verbosity:\t{}".format(args.verbose))
	log.all("Nb of workers:\t{}".format(plugin.max_workers))
	log.all("Ip range:\t{}:{}".format(plugin.ip_range, plugin.port))
	log.all("Transmit rate:\t{}".format(plugin.max_rate))
	log.all("Relative urls:\t{}".format(plugin.relative_url))
	log.all("Allow redirects:\t{}".format(plugin.allow_redirects))
	log.all("Verify ssl:\t{}".format(plugin.verify_ssl))
	log.all("#############################################")

def run_zmap(command):
	process = Popen(command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
	while True:
		line = process.stdout.readline().rstrip()
		if not line:
			break
		yield line

def main(plugin):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)
	command = "./masscan/bin/masscan {} -p{} --excludefile ./blacklist.txt --max-rate {}".format(plugin.ip_range, plugin.port, plugin.max_rate)
	try:
		for path in run_zmap(command):
			log.debug("Pushing {}".format(path.decode("utf-8")))
			workers.push(path.decode("utf-8"))
		log.all("MAsscan stopped ..")
		workers.stop()
	except ServiceExit:
		log.all("Wait, program is quitting :) .......")
		workers.stop()
		#os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def load_plugin(module):
	module_path = 'plugins.' + module
	if module_path in sys.modules:
		return sys.modules[module_path]
	return __import__(module_path, fromlist=[module])

def entrypoint():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--server", help="run in production mode", action="store_true")
	parser.add_argument("-d", "--dest", type=ip_address, help="Test with a given IP address")
	parser.add_argument("-p", "--plugin", type=str, help="Use a specific plugin (default: livebox-20377)", default='livebox-20377')
	parser.add_argument('-v', '--verbose', action='count', default=0)
	args = parser.parse_args()

	mod = load_plugin(args.plugin)
	plugin = mod.Plugin()
	plugin.config()
	if args.server:
		plugin.serverConf()
	if args.dest:
		plugin.ip_range = args.dest
	log.__setup__(args.verbose)
	print_config(plugin, args)
	workers.init(plugin)
	main(plugin)

if __name__ == '__main__':
	if os.geteuid() != 0:
		os.execvp("sudo", ["sudo"] + sys.argv)	
	entrypoint()