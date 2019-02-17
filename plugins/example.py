#!/usr/bin/env python3.5

"""
*---------------*
|CVE-EXAMPLE    |
*---------------*

This is an example plugin implementation

# Class variables are defined by default in the interface (IPlugin.py)
# Thoses variables can be modified in the __init__ function
#
# @type	{variable name}		default_value	Explanation
# @int  {max_workers}		2				number of threads used during the scanning process
# @int  {timeout}			5				Duration a thread should wait for the response
# @bool {allow_redirects}	True			allow http redirects (code 3XX)
# @bool	{verify_ssl}		False			verify ssl certificates
# @str	{relative_url}		/				Requested url for web-based plugins
# @str	{port}				8080			#TODO: remove this

"""

from plugins.IPlugin import IPlugin

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
	# @param {res} Requests object
	# @return {None} No returns expected
	def exec(self, data):
		pass