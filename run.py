#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from app import app
from core.main import entrypoint as coreService
import os
import sys


if __name__ == "__main__":
	if os.geteuid() != 0:
		os.execvp("sudo", ["sudo"] + sys.argv)
	if  len(sys.argv) > 1 and sys.argv[1] == "--webserver":
		app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)
	else:
		print("")
		coreService()
