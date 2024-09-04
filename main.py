import curses
from utils.system import config
from modules.actions import *
from modules.curses.Menu import Menu
from modules.curses.MenuItem import MenuItem

def main(stdscr):
    config.initialize(stdscr)

    items = [
        MenuItem("VALIDATE_ENVIRONMENT", validate_environment),
        MenuItem("EXIT", quit_program)
    ]
    footer_items = []

    Menu(stdscr, "TITLE_MENU", "SUBTITLE_MENU", items, footer_items).run()

if __name__ == "__main__":
    curses.wrapper(main)