#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

"""
*----------------*
|CVE-2018-15473  |
*----------------*
Sources:
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-15473
https://security.netapp.com/advisory/ntap-20181101-0001/
https://www.exploit-db.com/exploits/45233
https://github.com/Rhynorater/CVE-2018-15473-Exploit

"""
import core.logger as log
from plugins.IPlugin import IPlugin, connection_type

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 22
		self.connection_type = connection_type.RAW

	def config(self):
		pass

	def exec(self, connection):
		log.info("Running my custom plugin")
		pass