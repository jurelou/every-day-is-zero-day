#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import inspect
import datetime
from .plugins.IPlugin import connection_type

v_level = ""

def __setup__(level):
	global v_level
	v_level = level
	pass;

def all(*kwargs):
	[sys.stdout.write(' ' + str(i)) for i in kwargs]
	sys.stdout.write('\n')

def info(*kwargs):
	sys.stdout.write("[ALL]")
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	sys.stdout.write("[INFO {}]".format(mod.__name__.split(".")[1]))
	[sys.stdout.write(' ' + str(i)) for i in kwargs]
	sys.stdout.write('\n')

def debug(*kwargs):
	if v_level >= 2:
		sys.stdout.write("[DEBUG]")
		[sys.stdout.write(' ' + str(i)) for i in kwargs]
		sys.stdout.write('\n')

def err(*kwargs):
	if v_level >= 1:
		frm = inspect.stack()[1]
		mod = inspect.getmodule(frm[0])
		sys.stdout.write("[ERROR]")
		[sys.stdout.write(' ' + str(i)) for i in kwargs]
		sys.stdout.write('{:>27s}:{}\n'.format(mod.__name__, inspect.stack()[1].function))

def critical(*kwargs):
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	sys.stdout.write("[CRITICAL]")
	[sys.stdout.write(' ' + str(i)) for i in kwargs]
	sys.stdout.write('{:>27s}:{}\n'.format(mod.__name__, inspect.stack()[1].function))

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