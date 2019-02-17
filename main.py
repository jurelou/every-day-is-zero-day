#!/usr/bin/env python3.5

"""

http://173.44.204.234:8080/
http://109.241.165.147:8080/Docsis_system.asp

"""

import sys
import signal
import time
import requests
from bs4 import BeautifulSoup
from worker import Queue
from xml.etree.cElementTree import iterparse

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':ADH-AES128-SHA256'
requests.packages.urllib3.disable_warnings() 

global PLUGIN
PORT = ':8080'
NB_ITER = 0
MAX_ITER = 300
MAX_WORKERS = 200

workers = Queue(MAX_WORKERS)

class ServiceExit(Exception):
	pass

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

class DynamicImporter:
    def __init__(self, module_name, class_name):
        module = __import__(module_name)
        my_class = getattr(module, class_name)
        instance = my_class()
        print (instance)

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
	res = get_from_addr(addr)
	if res:
		print ('Got response: %d from %s', res.status_code, addr)
		page = BeautifulSoup(res.text, 'html.parser')
		find_forms(page)

def parse_xml(elem):
	if elem.tag == 'host':
		global NB_ITER
		NB_ITER = NB_ITER + 1
		addr = elem.getchildren()[0].get('addr')
		workers.push(addr)	
	
def loop(file):
	[parse_xml(elem) for event, elem in iterparse(file)]

def main(file, plugin='toto'):
	signal.signal(signal.SIGTERM, service_shutdown)
	signal.signal(signal.SIGINT, service_shutdown)
	workers.init(plugin)
	try:
		loop(file)
		while True:
			time.sleep(0.5)
	except ServiceExit:
		print("Service exit")
		workers.stop()

if __name__ == '__main__':
	if len(sys.argv) is 2:
		main("scan.xml", sys.argv[1])
	else:
		main("scan.xml")