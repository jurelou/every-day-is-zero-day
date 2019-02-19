#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys
import inspect

file = ""

def __setup__(config):
	global file
	file = config["file"]
	pass;


def info(*kwargs):
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	sys.stdout.write("[INFO]")
	[sys.stdout.write(' ' + str(i)) for i in kwargs]
	#sys.stdout.write('{:>27s}:{}\n'.format(mod.__name__, inspect.stack()[1].function))
	sys.stdout.write('\n')

def err(*kwargs):
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	sys.stdout.write("[ERROR]")
	[sys.stdout.write(' ' + str(i)) for i in kwargs]
	sys.stdout.write('{:>27s}:{}\n'.format(mod.__name__, inspect.stack()[1].function))