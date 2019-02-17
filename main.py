#!/usr/bin/env python2.7

"""
http://173.44.204.234:8080/

http://109.241.165.147:8080/Docsis_system.asp
"""
import sys
import requests
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':ADH-AES128-SHA256'

from xml.etree.cElementTree import iterparse
from bs4 import BeautifulSoup

PORT = ':8080'
NB_ITER = 0
MAX_ITER = 2

def find_forms(page):
	form = page.find('form')
	if not form:
		print '>No forms found'
		return
	print page
	fields = form.findAll('input')
	if fields:
		print '>Found fields:',fields
		return
	print '>No fields found'

def get_from_addr(addr):
	r = None
	try:
		r = requests.get('http://' + addr + PORT, allow_redirects=True)
	except requests.exceptions.SSLError:
		try:
			r = requests.get('https://' + addr + PORT, verify=False, allow_redirects=True)
		except:
			print 'Failed to send https request to ', addr
	except requests.exceptions.ReadTimeout:
		print 'timeout from ', addr
	except:
		print 'Failed to send http request to ', addr
	return r

def analyse(addr):
	global NB_ITER
	NB_ITER = NB_ITER + 1

	res = get_from_addr(addr)
	if res:
		print 'Got response:', res.status_code,' from ',addr
		page = BeautifulSoup(res.text, 'html.parser')
		find_forms(page)
	if NB_ITER > MAX_ITER:
		exit()

def parse_xml(elem):
	if elem.tag == 'host':
		addr = elem.getchildren()[0].get('addr')
		analyse(addr)

def loop(file):
	[parse_xml(elem) for event, elem in iterparse(file)]

if __name__ == '__main__':
	if len(sys.argv) is 2:
		analyse(sys.argv[1])
	else:
		loop("scan.xml")