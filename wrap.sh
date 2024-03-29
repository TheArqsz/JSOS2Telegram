#!/bin/bash

# If you want to use this script in cron, you have to uncomment lines below and fill them with values
# export TG_TOKEN=
# export TG_CHAT_ID=
# export JSOS_USERNAME=
# export JSOS_PASSWORD=


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
id=`ps aux | grep "jsos2telegram" | grep -v 'grep' | awk '{print $2}'`
if [ ! -z "$id" ]; then
        echo "Killing $id"
        kill -9 $id
fi

python3 $SCRIPT_DIR/jsos2telegram.py