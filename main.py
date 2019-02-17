#!/usr/bin/env python3.5

"""

http://173.44.204.234:8080/
http://109.241.165.147:8080/Docsis_system.asp

"""

import sys
import requests
from q import Queue
from xml.etree.cElementTree import iterparse
from bs4 import BeautifulSoup
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':ADH-AES128-SHA256'
requests.packages.urllib3.disable_warnings() 

PORT = ':8080'
NB_ITER = 0
MAX_ITER = 5
NUM_THREADS = 20

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

def get_from_addr(addr):
	r = None
	try:
		r = requests.get('http://' + addr + PORT, allow_redirects=True, timeout=5, verify=False)
	except requests.exceptions.SSLError:
		print ('SSLError from %s', addr)
	except requests.exceptions.ReadTimeout:
		print ('timeout from %s', addr)
	except:
		print ('Failed to send http request to %s', addr)
	return r

def analyse(addr):
	global NB_ITER
	NB_ITER = NB_ITER + 1

	res = get_from_addr(addr)
	if res:
		print ('Got response: %d from %s', res.status_code, addr)
		page = BeautifulSoup(res.text, 'html.parser')
		find_forms(page)
	if NB_ITER > MAX_ITER:
		exit()

def parse_xml(elem):
	if elem.tag == 'host':
		addr = elem.getchildren()[0].get('addr')
		qpush(addr)

def loop(file):
	[parse_xml(elem) for event, elem in iterparse(file)]

def main(file):
	queue = Queue()
	#loop(file)

if __name__ == '__main__':
	if len(sys.argv) is 2:
		analyse(sys.argv[1])
	else:
		main("scan.xml")