#!/usr/bin/env python3.5

from bs4 import BeautifulSoup

def find_forms(page):
	form = page.find('form')
	if not form:
		print ('>No forms found')
		return
	fields = form.findAll('input')
	if fields:
		print ('>Found fields: {}',fields)
		return
	print ('>No fields found')

class Plugin():
	def __init__(self):
		self.max_workers = 2
		self.timeout = 5
		self.port = '8080'
		self.allow_redirects = True
		self.verify_ssl = False
		pass
	def config(self):
		pass
	def exec(self, res):
		print(res.status_code, res.url)
		page = BeautifulSoup(res.text, 'html.parser')
		find_forms(page)