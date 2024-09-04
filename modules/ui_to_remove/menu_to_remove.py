import curses
from utils.system import config

class MenuItem:
    def __init__(self, text, action, color_pair=4):
        self.text = text
        self.action = action
        self.color_pair = curses.color_pair(color_pair)

class Menu:
    def __init__(self, stdscr, items, label="", box_color_pair=5, label_color_pair=5, selected_color_pair=4, additional_buttons=None):
        self.stdscr = stdscr
        self.items = items
        self.label = label
        self.box_color_pair = curses.color_pair(box_color_pair)
        self.label_color_pair = curses.color_pair(label_color_pair)
        self.selected_color_pair = curses.color_pair(selected_color_pair)
        self.current_row = 0
        self.additional_buttons = additional_buttons if additional_buttons else []
    
    def display(self):
        height, width = self.stdscr.getmaxyx()
        
        # Center the window label
        x_pos = (width // 2) - (len(self.label) // 2)
        self.stdscr.attron(self.box_color_pair)
        self.stdscr.box()
        self.stdscr.attroff(self.box_color_pair)
        self.stdscr.addstr(0, x_pos, self.label, self.label_color_pair | curses.A_BOLD)

        for idx, item in enumerate(self.items):
            x = 2
            y = 2 + idx
            if idx == self.current_row:
                self.stdscr.attron(self.selected_color_pair)
                self.stdscr.addstr(y, x, item.text)
                self.stdscr.attroff(self.selected_color_pair)
            else:
                self.stdscr.addstr(y, x, item.text)

        # Display additional buttons at the bottom
        for idx, button in enumerate(self.additional_buttons):
            x = 2
            y = height - len(self.additional_buttons) + idx - 2
            if len(self.items) + idx == self.current_row:
                self.stdscr.attron(self.selected_color_pair)
                self.stdscr.addstr(y, x, button.text)
                self.stdscr.attroff(self.selected_color_pair)
            else:
                self.stdscr.addstr(y, x, button.text)
        
        self.stdscr.refresh()

    def display_clean(self):
        self.stdscr.clear()
        self.display()


    def handle_input(self):
        key = self.stdscr.getch()

        if key == curses.KEY_UP and self.current_row > 0:
            self.current_row -= 1
        elif key == curses.KEY_DOWN and self.current_row < len(self.items) + len(self.additional_buttons) - 1:
            self.current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if self.current_row < len(self.items):
                self.items[self.current_row].action(self.stdscr)
            else:
                self.additional_buttons[self.current_row - len(self.items)].action(self.stdscr)

    
    def run(self):
        self.display_clean()
        while not config.SHOULD_QUIT:
            self.handle_input()
            self.display()
      