import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from logging import DEBUG, debug, error
from urllib3.exceptions import MaxRetryError
from const import SHORT_WAIT_TIME, TG_CHAT_ID, TG_MESSAGE_URL, TG_PHOTO_URL

import random
import requests


def element_exists(driver: WebDriver, css_selector: str) -> bool:
    try:
        driver.find_element_by_css_selector(css_selector=css_selector)
        debug(f"Element {css_selector} exists")
        return True
    except NoSuchElementException:
        debug(f"Element {css_selector} does not exist")
        return False


def wait_for_url_by_element_selector(driver: WebDriver, url: str, css_selector: str, delay: int = 10*SHORT_WAIT_TIME):
    try:
        _ = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        debug(f"URL {url} loaded")
    except TimeoutException:
        error(f"URL {url} took too long to load")
        raise Exception(f"URL {url} took too long to load")


def type_in_input_by_selector(driver: WebDriver, css_selector: str, content: str):
    tries = 0
    while tries < 5:
        if element_exists(driver=driver, css_selector=css_selector):
            element = driver.find_element_by_css_selector(
                css_selector=css_selector)
            break
        else:
            sleep(5)
            tries += 1
        if tries == 5:
            raise Exception(f"Element {css_selector} not found")
    for char in content:
        start = 0.01
        stop = 0.3
        step = 0.05
        precision = 0.01
        f = 1 / precision
        n = random.randrange(start * f, stop * f, step * f) / f
        sleep(n)
        element.send_keys(char)


def submit_entry(driver: WebDriver, css_selector: str):
    element = driver.find_element_by_css_selector(css_selector=css_selector)
    if element is None:
        raise Exception(f"Element {css_selector} not found")
    element.send_keys(Keys.ENTER)


def clean_driver(driver: WebDriver):
    try:
        driver.quit()
    except MaxRetryError:
        debug("Cannot quit driver")
    finally:
        exit(0)


def escape_chars(text: str) -> str:
    chars = ['_', '*', '[', ']',
             '(', ')', '~', '`', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for c in chars:
        text = text.replace(c, f"\\{c}")
    return text


def send_photo(chat_id, image_path, image_caption=""):
    data = {
                "chat_id": str(TG_CHAT_ID),
                "caption": image_caption
        }
    data = {"chat_id": chat_id, "caption": image_caption}
    with open(image_path, "rb") as image_file:
        ret = requests.post(TG_PHOTO_URL, data=data, files={"photo": image_file})
    return ret.json()


def send_debug_message_by_tg(message: str, t: str = 'DEBUG'):
    if LOG_LEVEL == DEBUG:
        data = {
            "chat_id": str(TG_CHAT_ID),
            "text": message,
            "parse_mode": "html"
        }
        r = requests.post(TG_URL, json=data)
        if r.status_code == 200:
            debug(f"{t} Telegram message sent")
        else:
            debug(f"Message {message} not sent. Error: {r.content}")


def send_message_by_tg(message: str, t: str = 'INFO'):
    data = {
        "chat_id": str(TG_CHAT_ID),
        "text": message,
        "parse_mode": "html"
    }
    r = requests.post(TG_URL, json=data)
    if r.status_code == 200:
        debug(f"{t} Telegram message sent")
    else:
        debug(f"Message {message} not sent. Error: {r.content}")


def send_messages_by_tg(messages: list):
    for m in messages:
        text = (f"<b>From</b>: <code>{m.get('from')}</code>\n"
                f"<b>When</b>: <code>{m.get('when')}</code>\n"
                f"<b>Topic</b>: <code>{m.get('topic')}</code>\n"
                f"<b>Message</b>: \n{m.get('text')}"
                )
        debug(f"Sending a message from {m.get('from')}")
        send_message_by_tg(message=text, t="JSOS")
