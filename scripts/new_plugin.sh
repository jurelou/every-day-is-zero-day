#!/bin/sh
if [ $# -ne 1 ]
  then
    echo "Give me your plugin name!"
fi

cp  ./core/plugins/example.py ./core/plugins/$1.py
