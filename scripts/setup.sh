#!/bin/sh
cd masscan && make -j4
cd ..
virtualenv venv
source venv/bin/activate
venv/bin/pip install -r requirements.txt
