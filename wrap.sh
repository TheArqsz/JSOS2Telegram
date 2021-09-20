#!/bin/bash

id=`ps aux | grep edurun | grep -v 'grep' | awk '{print $2}'`
if [ ! -z "$id" ]; then
	echo "Killing $id"
	kill -9 $id
fi

python3 /tmp/edukascrap/edurun.py
