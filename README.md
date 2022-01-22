# JSOS2Telegram bridge

## Installation

```bash
sudo apt install firefox-geckodriver firefox python3 python3-pip
sudo python3 -m pip install -r requirements.txt
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
python3 main.py
```

### Help

To check parameters for the script use:
```bash
python3 main.py -h
```
