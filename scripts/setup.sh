#!/bin/bash
cd masscan && make -j4
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt