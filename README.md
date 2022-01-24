# JSOS2Telegram bridge

[![Linting](https://github.com/TheArqsz/JSOS2Telegram/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/TheArqsz/JSOS2Telegram/actions)
[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue?style=flat&logo=python)](https://www.python.org/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

This version doesn't use selenium. It handles plain HTTP/S requests to JSOS. To check version that does use selenium and webbrowser, take a look at branch [selenium](/tree/selenium)

## Installation

```bash
python3 -m pip install -r requirements.txt
chmod +x wrap.sh
```

## Telegram data

### Chat ID

Access [@RawDataBot](https://telegram.me/RawDataBot) via Telegram and collect `message.chat.id`. Save it for later.

### Bot API token

Open [@BotFather](https://telegram.me/BotFather) and create new Bot. Name it whatever you want (as long as it matches the Telegram policy). Collect its API token (save it for later).

## Environmental variables

```bash
export JSOS_USERNAME=xxx
export JSOS_PASSWORD=xxx
export TG_TOKEN=xxx
export TG_CHAT_ID=xxx
```
where `TG_CHAT_ID` is an ID that we collected in step [`Chat ID`](#chat-id), `TG_TOKEN` is a [bot API token](#bot-api-token) and `JSOS_USERNAME` and `JSOS_PASSWORD` are credentials for a JSOS.

## Usage

```bash
wrap.sh
```
or
```bash
python3 jsos2telegram.py
```

### Help

To check parameters for the script use:
```bash
python3 jsos2telegram.py -h
```
