import os
import curses
from .loaders import load_language, load_theme

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

    load_language(INTERFACE_LANGUAGE)
    load_theme(THEME)

    stdscr.nodelay(1)
    stdscr.keypad(True)

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.start_color()
    for idx, (key, (fg, bg)) in enumerate(COLOR_PAIRS.items(), start=1):
        curses.init_pair(idx, fg, bg)