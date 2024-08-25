import curses
import os
from os import path
from . import config

BASE_CONFIG_PATH = path.abspath(path.join(path.dirname(__file__), "..", "..", "config"))


def load_language(language):
    config.LANGUAGE_STRINGS
    language_file = BASE_CONFIG_PATH + f"/languages/{language}.lang"
    with open(language_file, 'r') as file:
        for line in file:
            if line.startswith("#") or not line.strip():
                continue
            key, value = line.strip().split("=")
            config.LANGUAGE_STRINGS[key] = value

def load_theme(theme):
    theme_file = BASE_CONFIG_PATH + f"/themes/{theme}.theme"
    with open(theme_file, 'r') as file:
        for idx, line in enumerate(file, start=1):
            key, value = line.strip().split("=")
            fg, bg = value.split(",")
            config.COLOR_PAIRS[key] = (getattr(curses, f"COLOR_{fg}"), getattr(curses, f"COLOR_{bg}"))
            curses.init_pair(idx, config.COLOR_PAIRS[key][0], config.COLOR_PAIRS[key][1])