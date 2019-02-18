#!/bin/sh
pip install requirements.txt || pip3 install requirements.txt
cd masscan && make -j4
