#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

"""
*---------------*
|CVE-EXAMPLE    |
*---------------*

This is an example plugin implementation

"""
import core.logger as log
from plugins.IPlugin import IPlugin

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 22
		self.max_workers = 1
		self.connection_type = connection_type.RAW

	# This function will be used in the future to add additional configuration
	#
	# @return {None} No returns expected
	def config(self):
		pass
	# This function is called each time our scanned finds a valid host
	#
	# @param {res} Requests object
	# @return {None} No returns expected
	def exec(self, data):
		log.info("Running my custom plugin")
		pass