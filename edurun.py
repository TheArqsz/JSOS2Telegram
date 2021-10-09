from const import (
    LONG_WAIT_TIME, MAX_LOGIN_TRIES,
    VERY_LONG_WAIT_TIME, LOG_LEVEL
)
from edukacja import (
    access_all_messages, get_unread_messages, is_edukacja_online,
    is_user_logged_in, login, logout
)
from helpers import (
    clean_driver, delete_screenshot, make_screenshot, send_debug_message_by_tg, send_message_by_tg,
    send_messages_by_tg, send_photo
)

from time import sleep, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from logging import (
    ERROR, basicConfig,
    debug, exception, info,
    getLogger, FileHandler, StreamHandler
)

basicConfig(
    format="[%(name)s] {%(pathname)s:%(lineno)d} %(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=LOG_LEVEL,
    handlers=[
        FileHandler(f"jsos2telegram-{int(time())}.log"),
        StreamHandler()
    ]
)
getLogger('urllib3.connectionpool').setLevel(ERROR)
getLogger('urllib3.util.retry').setLevel(ERROR)
getLogger('selenium.webdriver.remote.remote_connection').setLevel(ERROR)
getLogger('urllib3.connectionpool').setLevel(ERROR)

options = Options()
options.headless = True

driver = None

info("Starting the app")
send_debug_message_by_tg(message="<b>Status message</b>: Starting the app")

try:
    while True:
        if not is_edukacja_online():
            debug(f"Edukacja is offline. Sleeping for {VERY_LONG_WAIT_TIME}")
            sleep(VERY_LONG_WAIT_TIME)
            continue
        driver = webdriver.Firefox(options=options)
        # Login
        tries = 0
        while not is_user_logged_in(driver=driver) and tries < MAX_LOGIN_TRIES:
            tries += 1
            logged = login(driver=driver)
            if not logged:
                debug(
                    f"Trying to log in once more. Tries left - {MAX_LOGIN_TRIES - tries}")
        if not is_user_logged_in(driver=driver):
            debug(f"Cannot log in. Sleeping for {VERY_LONG_WAIT_TIME}")
            sleep(VERY_LONG_WAIT_TIME)
            continue

        # Check messages
        _status = access_all_messages(driver=driver)
        if not _status:
            raise Exception("Cannot access messages")
        unread = get_unread_messages(driver=driver)

        # Log out
        _status = logout(driver=driver)
        if not _status:
            raise Exception("Cannot log out")

        # Send by tg
        send_messages_by_tg(messages=unread)
        try:
            driver.quit()
        except Exception:
            pass
        debug(f"Sleeping for {LONG_WAIT_TIME}")
        sleep(LONG_WAIT_TIME)
except KeyboardInterrupt as e:
    info("Keyboard interrupt raised - cleaning driver and exiting")
    clean_driver(driver=driver)
except Exception as e:
    exception(e)
    path = make_screenshot(driver=driver)
    send_photo(image_path=path,
               image_caption=f"Error <code>{e}</code> occured. Current state of website as in screenshot")
    delete_screenshot(path=path)
finally:
    clean_driver(driver=driver)
