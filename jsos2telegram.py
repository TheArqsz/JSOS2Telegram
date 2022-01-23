from bridge import Bridge
from const import JSOS_USERNAME, JSOS_PASSWORD
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--username', '-u', dest='jsos_username', type=str, required=False)
parser.add_argument('--password', '-p', dest='jsos_password', type=str, required=False)

args = parser.parse_args()

jsos_username = args.jsos_username if args.jsos_username else JSOS_USERNAME
jsos_password = args.jsos_password if args.jsos_password else JSOS_PASSWORD

with Bridge(jsos_username=jsos_username, jsos_password=jsos_password) as j:
    j.loop()
