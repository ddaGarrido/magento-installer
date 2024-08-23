import curses
import subprocess
import re

def init_screen():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(1)
    stdscr.keypad(True)
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
    return stdscr

def end_screen(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

# Display a message box
def show_message(win, title, message, color_pair=0):
    height, width = win.getmaxyx()
    box_height = 10
    box_width = width - 4
    box_win = curses.newwin(box_height, box_width, (height - box_height) // 2, 2)
    box_win.clear()
    box_win.attron(curses.color_pair(5))
    box_win.box()
    box_win.attroff(curses.color_pair(5))
    box_win.addstr(0, 2, f" {title} ", curses.color_pair(5) | curses.A_BOLD)
    box_win.addstr(2, 2, message[:box_width-4], curses.color_pair(color_pair))
    box_win.refresh()
    box_win.getch()