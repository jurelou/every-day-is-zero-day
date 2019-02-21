#!/bin/bash
cd ../masscan && make -j4
if [ $? -eq 2 ]; then
    cd .. ; rm -rf masscan
    git clone https://github.com/robertdavidgraham/masscan.git ; cd masscan
    make -j4
fi

cd ..
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
