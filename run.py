#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from core.main import entrypoint as coreService

if __name__ == "__main__":
	if os.geteuid() != 0:
		os.execvp("sudo", ["sudo"] + sys.argv)
	coreService()
