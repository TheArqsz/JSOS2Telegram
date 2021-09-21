#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
id=`ps aux | grep edurun | grep -v 'grep' | awk '{print $2}'`
if [ ! -z "$id" ]; then
	echo "Killing $id"
	kill -9 $id
fi

python3 $SCRIPT_DIR/edurun.py
