import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from logging import debug, error
from urllib3.exceptions import MaxRetryError
from const import LONG_WAIT_TIME
from selenium.webdriver.remote.command import Command
import random
import tempfile
import os


def is_driver_working(driver: WebDriver) -> bool:
    try:
        driver.execute(Command.STATUS)
        logging.debug("Driver is working properly")
        return True
    except MaxRetryError:
        logging.debug("Driver is not working")
        return False


def element_exists(driver: WebDriver, css_selector: str) -> bool:
    try:
        driver.find_element_by_css_selector(css_selector=css_selector)
        debug(f"Element {css_selector} exists")
        return True
    except NoSuchElementException:
        debug(f"Element {css_selector} does not exist")
        return False


def wait_for_url_by_element_selector(driver: WebDriver, url: str, css_selector: str, delay: int = LONG_WAIT_TIME):
    try:
        debug(f"Waiting for {delay} for an element")
        _ = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        debug(f"URL {url} loaded")
        return True
    except TimeoutException:
        error(f"URL {url} took too long to load")
        return False


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


def clean_driver(driver: WebDriver, force_quit: bool = True):
    try:
        driver.quit()
    except MaxRetryError:
        debug("Cannot quit driver")
    finally:
        if force_quit:
            exit(0)


def escape_chars(text: str) -> str:
    chars = ['_', '*', '[', ']',
             '(', ')', '~', '`', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for c in chars:
        text = text.replace(c, f"\\{c}")
    return text


def make_screenshot(driver: WebDriver, delete_on_make=False):
    path = None
    with tempfile.NamedTemporaryFile(suffix='.png', delete=delete_on_make) as tmp:
        path = tmp.name
        try:
            debug("Taking a screenshot")
            driver.save_screenshot(path)
            debug(f"Screenshot saved as {path}")
        except Exception:
            error("Cannot take a screenshot")
    return path


def delete_screenshot(path: str):
    if os.path.exists(path):
        debug(f"Deleting file {path}")
        os.remove(path)
