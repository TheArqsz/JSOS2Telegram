from const import (
    LONG_WAIT_TIME, MAX_LOGIN_TRIES, 
    VERY_LONG_WAIT_TIME, LOG_LEVEL
)
from edukacja import (
    access_all_messages, get_unread_messages, 
    is_user_logged_in, login, logout
)
from helpers import (
    clean_driver, send_message_by_tg, 
    send_messages_by_tg
)

from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from logging import (
    ERROR, basicConfig, 
    debug, exception, info, 
    getLogger
)

basicConfig(
    format="[%(name)s] {%(pathname)s:%(lineno)d} %(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level = LOG_LEVEL
)
getLogger('urllib3.connectionpool').setLevel(ERROR)
getLogger('urllib3.util.retry').setLevel(ERROR)
getLogger('selenium.webdriver.remote.remote_connection').setLevel(ERROR)
getLogger('urllib3.connectionpool').setLevel(ERROR)

options = Options()
options.headless = True

driver = None

info("Starting the app")

try:
    while True:
        driver = webdriver.Firefox(options=options)
        # Login
        tries = 0
        while not is_user_logged_in(driver=driver) and tries < MAX_LOGIN_TRIES:
            login(driver=driver)
            debug(f"Trying to log in once more. Tries left - {MAX_LOGIN_TRIES - tries}")
            tries += 1
        if not is_user_logged_in(driver=driver):
            debug(f"Cannot log in. Sleeping for {VERY_LONG_WAIT_TIME}")
            sleep(VERY_LONG_WAIT_TIME)

        # Check messages
        access_all_messages(driver=driver)
        unread = get_unread_messages(driver=driver)

        # Log out
        logout(driver=driver)

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
    send_message_by_tg(f"Exiting JSOS loop. Error {e} occured")
except BaseException as e:
    exception(e)
    send_message_by_tg(f"Exiting JSOS loop. Error {e} occured")
finally:
    clean_driver(driver=driver)