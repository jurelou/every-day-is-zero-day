#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys
import inspect

v_level = ""

def __setup__(level):
	global v_level
	v_level = level
	pass;

def all(*kwargs):
	sys.stdout.write("[ALL]")
	[sys.stdout.write(' ' + str(i)) for i in kwargs]
	sys.stdout.write('\n')

def info(*kwargs):
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
	if v_level is 1:
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