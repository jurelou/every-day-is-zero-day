#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import logging
from logging.handlers import RotatingFileHandler
from .plugins.IPlugin import connection_type
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

FORMAT_FILE = logging.Formatter(fmt='level=%(levelname)-8s %(message)s')
FORMAT = logging.Formatter(fmt='[%(levelname)-8s] %(message)s')
MAX_FILE_SIZE = 351000000

def __setup__(level, file):
	logging_level = logging.INFO if level == 0 else logging.DEBUG
	logger = logging.getLogger("")
	logger.setLevel(logging_level)
		
	if file:
		handler = RotatingFileHandler("/var/log/0dayz.log", maxBytes=MAX_FILE_SIZE, backupCount=5)
		handler.setFormatter(FORMAT_FILE)
		handler.setLevel(logging_level)
		logger.addHandler(handler)
	else:
		h = logging.StreamHandler()
		h.setLevel(logging_level)
		h.setFormatter(FORMAT)
		logger.addHandler(h)

def print_config(plugins, args):
	sys.stdout.write("######## Using the following config ########\n")
	sys.stdout.write("Verbosity:\t{}\n".format(args.verbose))
	sys.stdout.write("Threads:\t{}\n".format(args.threads))
	sys.stdout.write("Transmit rate:\t{}\n".format(args.max_rate))
	sys.stdout.write("IP range:\t{}\n".format(args.ip_range))
	sys.stdout.write("Plugin(s) enabled:\n")
	for port,name,plugin in plugins:
		sys.stdout.write("\t{}:\n".format(name))
		sys.stdout.write("\t\tport: {}\n".format(port))
		if plugin.connection_type == connection_type.WEB:
			sys.stdout.write("\t\trelative_url: {}\n".format(plugin.relative_url))
			sys.stdout.write("\t\tHTTP redirect: {}\n".format(plugin.allow_redirects))
			sys.stdout.write("\t\tVerify ssl: {}\n".format(plugin.verify_ssl))
	sys.stdout.write("#############################################\n")
