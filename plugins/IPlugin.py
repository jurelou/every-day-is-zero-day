class IPlugin():
	def __init__(self):
		# Number of threads used by the scanner
		self.max_workers = 5
		# Timeout after a request should be dropped
		self.timeout = 5
		# Allow http redirects (3xx)
		self.allow_redirects = True
		# Verify ssl certificate
		self.verify_ssl = False
		# Requested url
		self.relative_url = '/get_getnetworkconf.cgi'
		# Network segment that will be scanned
		# by default we are scanning all 4 bilion addresses
		self.ip_range = '0.0.0.0/0'
		# Maximum number of packets the scanner will send.
		# To avoid local network congestions it is recommanded to use a small number
		self.max_rate = 100
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