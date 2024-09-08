import os
from os import path
from dotenv import load_dotenv
from .loaders import load_language, load_theme
from utils.curses import initialize_curses

BASE_CONFIG_PATH = path.abspath(path.join(path.dirname(__file__), "..", ".."))
load_dotenv(BASE_CONFIG_PATH + "/.env")

# Global Variables
INTERFACE_LANGUAGE = None
MAGENTO_VERSIONS = None
API_TOKEN = None
THEME = None
SHOULD_QUIT = False
LANGUAGE_STRINGS = {}
COLOR_PAIRS = {}

def set_global_variables():
    global INTERFACE_LANGUAGE, INTERFACE_THEME, MAGENTO_VERSIONS, API_TOKEN, COLOR_PAIRS

    INTERFACE_LANGUAGE = os.getenv("INTERFACE_LANGUAGE", "en_US")
    INTERFACE_THEME = os.getenv("INTERFACE_THEME", "default")

    MAGENTO_VERSIONS = os.getenv("MAGENTO_VERSIONS", "2.4.3").split(",")
    API_TOKEN = os.getenv("API_TOKEN", "")

    os.environ["INTERFACE_LANGUAGE"] = INTERFACE_LANGUAGE

def initialize(stdscr):
    set_global_variables()

    load_language(INTERFACE_LANGUAGE)
    load_theme(INTERFACE_THEME)

    initialize_curses(stdscr)

def get_language_string(key):
    return LANGUAGE_STRINGS[key] if key in LANGUAGE_STRINGS else key