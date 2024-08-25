import os
import curses
from os import path
from dotenv import load_dotenv
from .loaders import load_language, load_theme

BASE_CONFIG_PATH = path.abspath(path.join(path.dirname(__file__), "..", ".."))
load_dotenv(BASE_CONFIG_PATH + "/environment.env")

# Global Variables
INTERFACE_LANGUAGE = None
MAGENTO_VERSIONS = None
API_TOKEN = None
THEME = None
SHOULD_QUIT = False
LANGUAGE_STRINGS = {}
COLOR_PAIRS = {}

def initialize(stdscr):
    global INTERFACE_LANGUAGE, MAGENTO_VERSIONS, API_TOKEN, THEME, COLOR_PAIRS

    INTERFACE_LANGUAGE = os.getenv("INTERFACE_LANGUAGE", "pt_BR")
    MAGENTO_VERSIONS = os.getenv("MAGENTO_VERSIONS", "2.4.3").split(",")
    API_TOKEN = os.getenv("API_TOKEN", "")
    THEME = os.getenv("THEME", "default")
    os.environ["INTERFACE_LANGUAGE"] = INTERFACE_LANGUAGE

    load_language(INTERFACE_LANGUAGE)
    load_theme(THEME)

    stdscr.nodelay(1)
    stdscr.keypad(True)

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.start_color()