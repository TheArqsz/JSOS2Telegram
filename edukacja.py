import requests
from logging import debug, error
from selenium.webdriver.remote.webdriver import WebDriver
from helpers import (
    element_exists,
    submit_entry, type_in_input_by_selector,
    wait_for_url_by_element_selector
)
from const import (
    EDU_LOGOUT_BUTTON_SELECTOR, EDU_USER_DETAILS_SELECTOR, EDU_WIADOMOSC_SELECTOR,
    EDU_ZAPISY_SELECTOR,
    JSOS_PASSWORD, JSOS_USERNAME,
    LOGIN_USER_URL, LOGOUT_USER_SELECTOR, MAIN_EDU_LOGIN_BUTTION_SELECTOR,
    MAIN_EDU_PASSWORD_INPUT_SELECTOR,
    MAIN_EDU_URL, MAIN_EDU_USERNAME_INPUT_SELECTOR,
    WIADOMOSCI_URL, WIADOMOSC_CONTENT_TEXT_SELECTOR,
    WIADOMOSC_EDU_LISTA, WIADOMOSC_EDU_NOWA_SELECTOR,
)


class EdukacjaError(Exception):
    pass


class CredentialsError(EdukacjaError):
    pass


def login(driver: WebDriver, username: str = JSOS_USERNAME, password: str = JSOS_PASSWORD):
    if JSOS_USERNAME == "" or JSOS_PASSWORD == "":
        error("Empty JSOS credentials - check them manually")
        raise CredentialsError("Empty JSOS credentials")
    driver.delete_all_cookies()
    driver.get(MAIN_EDU_URL)
    _loaded = wait_for_url_by_element_selector(
        driver=driver, url=MAIN_EDU_URL, css_selector=MAIN_EDU_USERNAME_INPUT_SELECTOR)
    if not _loaded:
        return False
    type_in_input_by_selector(
        driver=driver, css_selector=MAIN_EDU_USERNAME_INPUT_SELECTOR, content=username)
    type_in_input_by_selector(
        driver=driver, css_selector=MAIN_EDU_PASSWORD_INPUT_SELECTOR, content=password)
    submit_entry(driver=driver, css_selector=MAIN_EDU_PASSWORD_INPUT_SELECTOR)
    _loaded = wait_for_url_by_element_selector(
        driver=driver, url=LOGIN_USER_URL, css_selector=EDU_LOGOUT_BUTTON_SELECTOR)
    return _loaded


def is_user_logged_in(driver: WebDriver) -> bool:
    r1 = element_exists(driver=driver, css_selector=EDU_USER_DETAILS_SELECTOR)
    r2 = element_exists(driver=driver, css_selector=EDU_ZAPISY_SELECTOR)
    result = r1 and r2
    if result:
        debug("User is logged in")
    else:
        debug("User is not logged in")
    return result


def is_edukacja_online() -> bool:
    _h = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"  # noqa: E501
    }
    try:
        _r = requests.head(MAIN_EDU_URL, headers=_h)
        return _r.status_code == 200
    except Exception as e:
        print("****", e)
        debug(f"Cannot connect to {MAIN_EDU_URL}")
        return False


def logout(driver: WebDriver):
    debug("Logging user out")
    _loaded = wait_for_url_by_element_selector(
        driver=driver, url=MAIN_EDU_URL, css_selector=LOGOUT_USER_SELECTOR)
    if not _loaded:
        return _loaded
    submit_entry(driver=driver, css_selector=LOGOUT_USER_SELECTOR)
    _loaded = wait_for_url_by_element_selector(
        driver=driver, url=LOGIN_USER_URL, css_selector=MAIN_EDU_LOGIN_BUTTION_SELECTOR)
    return _loaded


def access_all_messages(driver: WebDriver):
    _loaded = wait_for_url_by_element_selector(
        driver=driver, url=LOGIN_USER_URL, css_selector=EDU_WIADOMOSC_SELECTOR)
    if not _loaded:
        return _loaded
    submit_entry(driver=driver, css_selector=EDU_WIADOMOSC_SELECTOR)
    _loaded = wait_for_url_by_element_selector(
        driver=driver, url=WIADOMOSCI_URL, css_selector=WIADOMOSC_EDU_NOWA_SELECTOR)
    return _loaded


def get_unread_messages(driver: WebDriver) -> list:
    list_of_messages = driver.find_elements_by_css_selector(
        css_selector=WIADOMOSC_EDU_LISTA)
    list_of_messages = list_of_messages[1:]  # Exclude header from list
    unread = list()
    raw_messages = list()
    processed_messages = list()
    for el in list_of_messages:
        # Find all unread messages by bold text
        _e_b = el.find_elements_by_css_selector('td > * b')
        _e_a = el.find_elements_by_css_selector('td > * a')  # Find all links
        if _e_b != []:
            raw_messages.append((_e_b, _e_a))
    for m_list, m_a in raw_messages:
        href = m_a[0].get_property('href')
        m_from = m_list[0].text
        m_topic = m_list[1].text
        m_when = m_list[3].text
        processed_messages.append((href, m_from, m_topic, m_when))

    for href, m_from, m_topic, m_when in processed_messages:
        driver.get(href)
        _loaded = False

        _tries = 0
        while not _loaded or _tries < 5:
            _loaded = wait_for_url_by_element_selector(
                driver=driver, url=href, css_selector=WIADOMOSC_CONTENT_TEXT_SELECTOR)
            _tries += 1
        if not _loaded:
            raise Exception("Cannot load element for message sending")
        cont = driver.find_element_by_css_selector(
            css_selector=WIADOMOSC_CONTENT_TEXT_SELECTOR)
        unread.append(
            {
                'text': cont.text,
                'from': m_from,
                'topic': m_topic,
                'when': m_when
            }
        )
    return unread
