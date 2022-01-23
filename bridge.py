from const import (
    GECKODRIVER_PATH, MAX_LOGIN_TRIES,
    VERY_LONG_WAIT_TIME, LOG_LEVEL
)
from edukacja import (
    CredentialsError, access_all_messages, get_unread_messages, is_edukacja_online,
    is_user_logged_in, login, logout
)
from helpers import (
    clean_driver, delete_screenshot, is_driver_working, make_screenshot
)

from telegram import (
    send_debug_message_by_tg, send_messages_by_tg, send_photo
)

from time import sleep, time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from logging import (
    ERROR, basicConfig,
    debug, exception, info,
    getLogger, FileHandler, StreamHandler
)


class Bridge(object):
    def __init__(
        self, headless: bool = True,
        jsos_username: str = None, jsos_password: str = None,
        sleep_time: int = VERY_LONG_WAIT_TIME
    ):
        self.options = Options()
        self.options.headless = headless
        self.driver = None
        self.unread = None
        self.screenshot_path = None
        self.jsos_username = jsos_username
        self.jsos_password = jsos_password
        self.sleep_time = sleep_time
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

    def stop(self, force_quit: bool = False):
        clean_driver(driver=self.driver, force_quit=force_quit)

    def _main_loop(self):
        while True:
            if not is_edukacja_online():
                debug(
                    f"Edukacja is offline. Sleeping for {VERY_LONG_WAIT_TIME}"
                )
                sleep(VERY_LONG_WAIT_TIME)
                continue
            if self.driver is None or not is_driver_working(driver=self.driver):
                self.driver = webdriver.Firefox(
                    options=self.options, executable_path=GECKODRIVER_PATH
                )
            # Login
            tries = 0
            while not is_user_logged_in(driver=self.driver) and tries < MAX_LOGIN_TRIES:
                tries += 1
                self.logged = login(
                    driver=self.driver, username=self.jsos_username, password=self.jsos_password
                )
                if not self.logged:
                    debug(
                        f"Trying to log in once more. Tries left - {MAX_LOGIN_TRIES - tries}"
                    )
            if not is_user_logged_in(driver=self.driver):
                debug(f"Cannot log in. Sleeping for {VERY_LONG_WAIT_TIME}")
                sleep(VERY_LONG_WAIT_TIME)
                continue

            # Check messages
            _status = access_all_messages(driver=self.driver)
            if not _status:
                raise Exception("Cannot access messages")
            self.unread = get_unread_messages(driver=self.driver)

            # Log out
            _status = logout(driver=self.driver)
            if not _status:
                raise Exception("Cannot log out")

            # Send by tg
            send_messages_by_tg(messages=self.unread)
            try:
                self.stop()
            except Exception:
                pass
            debug(f"Sleeping for {self.sleep_time}")
            sleep(self.sleep_time)

    def start(self):
        self.driver = webdriver.Firefox(
            options=self.options, executable_path=GECKODRIVER_PATH
        )

    def loop(self):
        info("Starting the app")
        send_debug_message_by_tg(
            message="<b>Status message</b>: Starting the app"
        )
        try:
            self._main_loop()
        except KeyboardInterrupt:
            info("Keyboard interrupt raised - cleaning driver and exiting")
            self.stop()
        except Exception as e:
            exception(e)
            if is_driver_working(driver=self.driver) and e.__class__ is not CredentialsError:
                self.screenshot_path = make_screenshot(driver=self.driver)
                send_photo(
                    image_path=self.screenshot_path,
                    image_caption=f"Error <code>{e}</code> occured. Current state of website as in screenshot"
                )
                delete_screenshot(path=self.screenshot_path)
            else:
                send_debug_message_by_tg(
                    message=f"Error {e} occured", t="ERROR")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop(force_quit=True)
