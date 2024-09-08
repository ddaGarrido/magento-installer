import curses

def initialize_curses(stdscr):
    stdscr.nodelay(1)
    stdscr.keypad(True)

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    curses.start_color()