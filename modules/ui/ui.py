import curses

def draw_border(stdscr, title=" System Setup "):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.border(0)
    stdscr.addstr(0, (width // 2) - (len(title) // 2), title, curses.color_pair(1))
    stdscr.refresh()

def show_menu(stdscr, menu, title):
    curses.curs_set(0)
    current_row = 0
    while True:
        stdscr.clear()
        draw_border(stdscr, title)
        height, width = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            x = (width // 2) - (len(row) // 2)
            y = height // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.addstr(y, x, row, curses.color_pair(2) | curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, row, curses.color_pair(2))
        
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return current_row
