#!/bin/bash
cd masscan && git checkout master && make -j4
cd ..
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
