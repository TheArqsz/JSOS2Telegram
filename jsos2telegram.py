from logging import FileHandler, StreamHandler, basicConfig
import logging
from time import sleep, time
from jsos import Jsos
from const import (
    JSOS_USERNAME, JSOS_PASSWORD,
    LOG_LEVEL, TG_TOKEN, TG_CHAT_ID
)
from telegram import Telegram
import argparse

basicConfig(
    format="[%(name)s] {%(pathname)s:%(lineno)d} %(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=LOG_LEVEL,
    handlers=[
        FileHandler(f"jsos2telegram-{int(time())}.log"),
        StreamHandler()
    ]
)
log = logging.getLogger('jsos2telegram')

parser = argparse.ArgumentParser()
parser.add_argument(
    '--username', '-u',
    dest='jsos_username',
    help="Username for jsos",
    type=str, required=False
)
parser.add_argument(
    '--password', '-p',
    dest='jsos_password',
    help='Password for jsos',
    type=str, required=False
)
parser.add_argument(
    '--bot-token', '-b',
    dest='bot_token',
    help="Telegram's bot's token",
    type=str, required=False
)
parser.add_argument(
    '--chat-id', '-c',
    dest='chat_id',
    help="Chat to which messages would be sent",
    type=str, required=False
)
parser.add_argument(
    "--wait-time", "-w",
    help="duration of wait time between scans",
    type=int, default=240
)

args = parser.parse_args()

jsos_username = args.jsos_username if args.jsos_username else JSOS_USERNAME
jsos_password = args.jsos_password if args.jsos_password else JSOS_PASSWORD
bot_token = args.bot_token if args.bot_token else TG_TOKEN
chat_id = args.chat_id if args.chat_id else TG_CHAT_ID
WAIT_TIME = args.wait_time

while True:
    with Jsos(username=jsos_username, password=jsos_password) as jsos, \
            Telegram(bot_token=bot_token, chat_id=chat_id) as tg:
        msgs = jsos.get_messages(max=3, only_unread=True)
        tg.send_messages_by_tg(messages=msgs)
    log.info(f"Sleeping for {WAIT_TIME} sec")
    try:
        sleep(WAIT_TIME)
    except KeyboardInterrupt:
        exit(1)
