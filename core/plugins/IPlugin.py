#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class connection_type():
	NONE = 0
	RAW = 1
	WEB = 2

class IPlugin():
	def __init__(self):
		# Number of threads used by the scanner
		self.connection_type = connection_type.NONE		# Timeout after a request should be dropped
		self.timeout = 5
		# Allow http redirects (3xx)
		self.allow_redirects = True
		# Verify ssl certificate
		self.verify_ssl = False
		# Requested url
		self.relative_url = '/get_getnetworkconf.cgi'
		# Port that will be checked
		self.port = 80

	# This function will be used in the future to add additional configuration 
	#
	# @return {None} Returns from this function is silenced
	def config(self):
		pass
	# This function is called each time our scanned finds a valid host
	#
	# @param {res} Requests object
	# @return {None} Returns from this function is silenced
	def exec(self, data):
		pass