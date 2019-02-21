#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*---------------*
|CVE-EXAMPLE    |
*---------------*

This is an example plugin implementation

# Class variables are defined by default in the interface (IPlugin.py)
# Thoses variables can be modified in the __init__ function
#

# @type	{variable name}		| default_value		|Explanation
------------------------------------------------------------------------------------------------
# @enum {connection_type}	| NONE			| This will determine the object send in the exec() method
				|			|	- connection_type.RAW: Will give you a raw tcp socket (https://docs.python.org/3/library/socket.html)
				|			|	- connection_type.WEB: Will give you a Requests object (http://docs.python-requests.org/en/master/)
# @int  {max_workers}		| 2			| number of threads used during the scanning process
# @bool	{verify_ssl}		| False			| verify ssl certificates
# @str  {ip_range}		| 0.0.0.0/0		| IP range to scan (only accept format with significant bits)
# @str	{port}			| 80			| Port which will be pinged on IP Addresses
# @str	{relative_url}		| /			| Requested url for web-based plugins (connection_type.WEB)
# @int  {timeout}		| 5			| Timeout for web-based plugins (connection_type.WEB)

"""
import core.logger as log
from plugins.IPlugin import IPlugin, connection_type

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()

	# This function will be used in the future to add additional configuration
	#
	# @return {None} No returns expected
	def config(self):
		pass
	# This function is called each time our scanned finds a valid host
	#
	# @param {res} 	It depends of your connection_type.
	#				- connection_type.RAW: Will give you a raw tcp socket (https://docs.python.org/3/library/socket.html)
	#				- connection_type.WEB: Will give you a Requests object (http://docs.python-requests.org/en/master/)
	# @return {None} No returns expected
	def exec(self, connection):
		log.info("Running my custom plugin")
		pass
