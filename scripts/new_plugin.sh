#!/bin/sh
if [ $# -ne 1 ]
  then
    echo "Give me your plugin name!"
fi

cp  ./plugins/example.py ./plugins/$1.py
