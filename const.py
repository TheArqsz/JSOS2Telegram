import os
from logging import DEBUG, INFO

JSOS_USERNAME = os.getenv("JSOS_USERNAME", "")
JSOS_PASSWORD = os.getenv("JSOS_PASSWORD", "")

TG_TOKEN = os.getenv("TG_TOKEN", "")
TG_MESSAGE_URL = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
TG_PHOTO_URL = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

LOG_LEVEL = DEBUG if os.getenv("LOG_LEVEL") == "DEBUG" else INFO

MAX_LOGIN_TRIES = 10
MAX_CHARS = 600

SHORT_WAIT_TIME = 5  # sec
WAIT_TIME = 20  # sec
LONG_WAIT_TIME = 300  # sec
VERY_LONG_WAIT_TIME = 1200

MAIN_EDU_BASE_URL = "https://edukacja.pwr.wroc.pl"
MAIN_EDU_URL = "https://edukacja.pwr.wroc.pl/EdukacjaWeb/studia.do"
LOGIN_USER_URL = "https://edukacja.pwr.wroc.pl/EdukacjaWeb/logInUser.do"
WIADOMOSCI_URL = "https://edukacja.pwr.wroc.pl/EdukacjaWeb/zawartoscSkrzynkiPocztowej.do"
MAIN_EDU_LOGIN_BUTTION_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.LEWA_KOMORKA > table > tbody > tr:nth-child(1) > td > table.LOGOWANIE > tbody > tr:nth-child(9) > td > input"
MAIN_EDU_USERNAME_INPUT_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.LEWA_KOMORKA > table > tbody > tr:nth-child(1) > td > table.LOGOWANIE > tbody > tr:nth-child(6) > td > input"
MAIN_EDU_PASSWORD_INPUT_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.LEWA_KOMORKA > table > tbody > tr:nth-child(1) > td > table.LOGOWANIE > tbody > tr:nth-child(8) > td > input"
EDU_LOGOUT_BUTTON_SELECTOR = '#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.LEWA_KOMORKA > table > tbody > tr:nth-child(1) > td > table.ZALOGOWANY > tbody > tr:nth-child(4) > td > table > tbody > tr > td:nth-child(4) > input[name="wyloguj"]'

EDU_USER_DETAILS_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.LEWA_KOMORKA > table > tbody > tr:nth-child(1) > td > table.ZALOGOWANY > tbody > tr:nth-child(3) > td"
EDU_ZAPISY_SELECTOR = '#cela1 > a[title="Zapisy"]'
EDU_WIADOMOSC_SELECTOR = '#cela1 > a[title="Wiadomości"]'
WIADOMOSC_EDU_NOWA_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.PRAWA_KOMORKA > table > tbody > tr > td > table:nth-child(7) > tbody > tr:nth-child(2) > td:nth-child(2) > form > input.PRZYCISK"
WIADOMOSC_EDU_LISTA = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.PRAWA_KOMORKA > table > tbody > tr > td > table.KOLOROWA > tbody > tr:nth-child(-n+5)"
WIADOMOSC_CONTENT_POWROT_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.PRAWA_KOMORKA > table > tbody > tr > td > center > form > input:nth-child(7)"
WIADOMOSC_CONTENT_TEXT_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.PRAWA_KOMORKA > table > tbody > tr > td > table.KOLOROWA > tbody > tr:nth-child(8) > td:nth-child(2)"

LOGOUT_USER_SELECTOR = "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.LEWA_KOMORKA > table > tbody > tr:nth-child(1) > td > table.ZALOGOWANY > tbody > tr:nth-child(4) > td > table > tbody > tr > td:nth-child(4) > input[name='wyloguj']"
