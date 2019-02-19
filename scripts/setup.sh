#!/bin/sh
pip3 install requirements.txt
chmod +x ./main.py
cd masscan && make -j4
