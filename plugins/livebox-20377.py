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

livebox:
*	http://89.129.126.167:8080/get_getnetworkconf.cgi
*	http://70.40.245.92:8080/get_getnetworkconf.cgi

"""
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
				if fields.has_key(input['name']) and value:
					fields[input['name']] = value
				if not fields.has_key(input['name']):
					fields[input['name']] = value
				continue
		if is_login_form:
			return action, fields
	return None, None

class Plugin(IPlugin):
	def __init__(self):
		super().__init__()
		self.max_workers = 1
		self.timeout = 10

	def config(self):
		pass

	def exec(self, res):
		page = BeautifulSoup(res.text, 'html.parser')
		if page:
			action, fields = find_forms(page)
			log.info(action, fields)