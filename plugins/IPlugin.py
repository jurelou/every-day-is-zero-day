class IPlugin():
	def __init__(self):
		# Number of threads used by the scanner
		self.max_workers = 2
		# Timeout for each Requests
		self.timeout = 5
		# TODO: moove this
		self.port = '8080'
		# Allow http redirects (3xx)
		self.allow_redirects = True
		# Verify ssl certificate
		self.verify_ssl = False
		# Requested url
		self.relative_url = '/'

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