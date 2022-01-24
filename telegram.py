import logging
import requests
from const import (
    LOG_LEVEL, TG_GET_CHAT_ENDPOINT,
    TG_MESSAGE_LIMIT, TG_CHAT_ID,
    TG_ROOT_URL, TG_SEND_MESSAGE_ENDPOINT,
    TG_SEND_PHOTO_ENDPOINT, TG_TOKEN
)
from logging import DEBUG

log = logging.getLogger('jsos2telegram')


class Telegram:

    def __init__(self, bot_token: str = TG_TOKEN, chat_id: int = TG_CHAT_ID):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.tg_root_url = f"{TG_ROOT_URL}{self.bot_token}"
        self.bot_verified = False
        self.chat_verified = False

    def __enter__(self):
        log.info("Starting connection with Telegram")
        self.verify_credentials()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        log.info("Closing connection with Telegram")
        self.bot_verified = False
        self.chat_verified = False

    def _send_get_message(self, endpoint: str, *args, **kwargs):
        _url = self.tg_root_url + endpoint
        return requests.get(_url, *args, **kwargs)

    def _send_post_message(self, endpoint: str, *args, **kwargs):
        _url = self.tg_root_url + endpoint
        return requests.post(_url, *args, **kwargs)

    def _is_verified(self):
        return self.bot_verified and self.chat_verified

    def verify_credentials(self):
        _r = self._send_post_message(
            endpoint=TG_GET_CHAT_ENDPOINT,
            json={
                "chat_id": self.chat_id
            }
        )
        _json = _r.json()
        self.bot_verified = _json.get(
            "ok", False) and _json['ok'] is True and _json.get('error_code', True) != 401
        self.chat_verified = _json.get(
            "ok", False) and _json['ok'] is True and _json.get('error_code', True) != 400

        if not self.chat_verified or not self.bot_verified:
            log.error("Telegram credentials are not valid")
            raise TelegramAuthenticationError(
                "Telegram credentials are not valid"
            )

        return self.bot_verified and self.chat_verified

    def escape_chars(self, text: str) -> str:
        chars = ['_', '*', '[', ']',
                 '(', ')', '~', '`', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for c in chars:
            text = text.replace(c, f"\\{c}")
        return text

    def send_photo(self, image_path: str, image_caption: str = ""):
        if not self._is_verified():
            raise TelegramAuthenticationError("Bot not authorized")
        data = {
            "chat_id": self.chat_id,
            "caption": image_caption[:TG_MESSAGE_LIMIT-1],
            "parse_mode": "html"
        }
        with open(image_path, "rb") as image_file:
            _r = self._send_post_message(
                endpoint=TG_SEND_PHOTO_ENDPOINT,
                data=data,
                files={"photo": image_file}
            )
            if _r.status_code == 200:
                log.debug("Telegram photo message sent")
            else:
                log.debug(f"Photo {image_path} not sent. Error: {_r.content}")

    def send_debug_message_by_tg(self, message: str, t: str = 'DEBUG'):
        if LOG_LEVEL == DEBUG:
            self.send_message_by_tg(message=message, t=t)

    def send_message_by_tg(self, message: str, t: str = 'log.info'):
        if not self._is_verified():
            raise TelegramAuthenticationError("Bot not authorized")
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "html"
        }
        _r = self._send_post_message(
            endpoint=TG_SEND_MESSAGE_ENDPOINT,
            json=data
        )
        if _r.status_code == 200:
            log.debug(f"{t} Telegram message sent")
        else:
            log.debug(f"Message {message} not sent. Error: {_r.content}")

    def send_messages_by_tg(self, messages: list):
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
            log.debug(f"Sending a message from {m.get('from')}")
            self.send_message_by_tg(message=text, t="JSOS")


class TelegramAuthenticationError(Exception):
    pass
