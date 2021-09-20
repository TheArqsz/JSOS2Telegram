# JSOS2Telegram bridge

## Installation

```bash
sudo apt install firefox-geckodriver firefox python3 
sudo python3 -m pip install requests selenium
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
where `TG_CHAT_ID` is an ID that we collected in step `Chat ID`, `TG_TOKEN` is a bot API token and `JSOS_USERNAME` and `JSOS_PASSWORD` are credentials for a JSOS.

## Run

```bash
wrap.sh
```
or
```bash
python3 edurun.py
```
