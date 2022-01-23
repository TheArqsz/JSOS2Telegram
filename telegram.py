import requests
from const import LOG_LEVEL, TG_MESSAGE_LIMIT, TG_CHAT_ID, TG_MESSAGE_URL, TG_PHOTO_URL
from logging import DEBUG, debug


def send_photo(image_path: str, image_caption: str = ""):
    data = {
        "chat_id": str(TG_CHAT_ID),
        "caption": image_caption[:TG_MESSAGE_LIMIT-1],
        "parse_mode": "html"
    }
    with open(image_path, "rb") as image_file:
        _r = requests.post(TG_PHOTO_URL, data=data,
                           files={"photo": image_file})
        if _r.status_code == 200:
            debug("Telegram photo message sent")
        else:
            debug(f"Photo {image_path} not sent. Error: {_r.content}")


def send_debug_message_by_tg(message: str, t: str = 'DEBUG'):
    if LOG_LEVEL == DEBUG:
        send_message_by_tg(message=message, t=t)


def send_message_by_tg(message: str, t: str = 'INFO'):
    data = {
        "chat_id": str(TG_CHAT_ID),
        "text": message,
        "parse_mode": "html"
    }
    _r = requests.post(TG_MESSAGE_URL, json=data)
    if _r.status_code == 200:
        debug(f"{t} Telegram message sent")
    else:
        debug(f"Message {message} not sent. Error: {_r.content}")


def send_messages_by_tg(messages: list):
    for m in messages:
        _message_text = m.get('text')
        if len(_message_text) > TG_MESSAGE_LIMIT - 1:
            _suffix = "\n\n<code>[Message redacted due to its length]</code>"
            _message_text = _message_text[:(
                TG_MESSAGE_LIMIT - 1 - len(_suffix))] + _suffix
        text = (f"<b>From</b>: <code>{m.get('from')}</code>\n"
                f"<b>When</b>: <code>{m.get('when')}</code>\n"
                f"<b>Topic</b>: <code>{m.get('topic')}</code>\n"
                f"<b>Message</b>: \n\n{_message_text}"
                )
        debug(f"Sending a message from {m.get('from')}")
        send_message_by_tg(message=text, t="JSOS")
