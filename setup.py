import curses
import subprocess
import re
import os

from utils.system import config
from utils.utils import show_message

class MenuItem:
    def __init__(self, text, action, color_pair=4):
        self.text = text
        self.action = action
        self.color_pair = curses.color_pair(color_pair)

class Menu:
    def __init__(self, stdscr, items):
        self.stdscr = stdscr
        self.items = items
        self.current_row = 0
    
    def display(self):
        height, width = self.stdscr.getmaxyx()
        win = curses.newwin(height - 2, width - 2, 1, 1)
        
        # Center the window label
        label = f" {config.LANGUAGE_STRINGS['MENU_TITLE']} "
        x_pos = (width // 2) - (len(label) // 2)
        win.attron(curses.color_pair(5))
        win.box()
        win.attroff(curses.color_pair(5))
        win.addstr(0, x_pos, label, curses.color_pair(5) | curses.A_BOLD)

        for idx, item in enumerate(self.items):
            x = 2
            y = 2 + idx
            if idx == self.current_row:
                win.attron(item.color_pair)
                win.addstr(y, x, item.text)
                win.attroff(item.color_pair)
            else:
                win.addstr(y, x, item.text)
        
        win.refresh()

        self.handle_input(win)

    def handle_input(self, win):
        key = self.stdscr.getch()

        if key == curses.KEY_UP and self.current_row > 0:
            self.current_row -= 1
        elif key == curses.KEY_DOWN and self.current_row < len(self.items) - 1:
            self.current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            self.items[self.current_row].action(win)

    
    def run(self):
        while not config.SHOULD_QUIT:
            self.display()
            

def check_service(service_name, regex, command=None):
    try:
        result = ""
        if not command:
            result = subprocess.check_output(f"{service_name} -v", shell=True, stderr=subprocess.STDOUT, text=True)
        else:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        if regex:
            match = re.search(regex, result)
            if match:
                return (True, match.group(0))
            else:
                return (False, result)
        else:
            return (True, result)
    except subprocess.CalledProcessError:
        return (False, "")

def validate_environment(win):
    win.clear()

    # Ask user for Magento version
    magento_versions = config.MAGENTO_VERSIONS
    win.addstr(2, 2, config.LANGUAGE_STRINGS["VALIDATE_ENVIRONMENT"], curses.color_pair(5))
    for idx, version in enumerate(magento_versions):
        x = 2
        y = 4 + idx
        if idx == 0:
            win.attron(curses.color_pair(4))
            win.addstr(y, x, version)
            win.attroff(curses.color_pair(4))
        else:
            win.addstr(y, x, version)
    win.addstr(4 + len(magento_versions), 2, "Pressione ENTER para confirmar", curses.color_pair(5))
    win.refresh()

    # Validate based on the selected Magento version
    # TODO: Implement Magento version validation
    
    services = {
        "nginx": ("([^\n]+)", None),
        "php": ("PHP ([^\n]+)", None),
        "mysql": ("mysql  Ver ([^\n]+)", "mysql --version"),
        "elasticsearch": ('"cluster_name" : "([^"]+)"', "curl -s -XGET 'http://localhost:9200'"),
        "composer": ("Composer version ([^\n]+)", "composer --version")
    }
    
    results = []
    
    for service, (regex, command) in services.items():
        status, result = check_service(service, regex, command)
        icon = "✔️" if status else "❌"
        color = curses.color_pair(2) if status else curses.color_pair(1)
        message = f"{icon} {service.upper()} {'INSTALADO' if status else 'NÃO INSTALADO'} - {result.strip()}"
        results.append((message, color))
    
    win.clear()
    win.attron(curses.color_pair(5))
    win.box()
    win.attroff(curses.color_pair(5))
    win.addstr(0, 2, " Resultados da Validação do Ambiente ", curses.color_pair(5) | curses.A_BOLD)
    
    for i, (message, color) in enumerate(results):
        win.addstr(i + 2, 2, message[:win.getmaxyx()[1] - 4], color)
    
    win.refresh()
    win.getch()

def quit_program(win):
    config.SHOULD_QUIT = True

def main(stdscr):
    config.initialize(stdscr)

    menu_items = [
        MenuItem(config.LANGUAGE_STRINGS["VALIDATE_ENVIRONMENT"], validate_environment),
        MenuItem(config.LANGUAGE_STRINGS["EXIT"], quit_program)
    ]

    menu = Menu(stdscr, menu_items)
    menu.run()

if __name__ == "__main__":
    curses.wrapper(main)
