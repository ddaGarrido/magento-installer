import curses
import subprocess
import re

from utils import init_screen, end_screen, show_message

SHOULD_QUIT = False

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
        
        win.attron(curses.color_pair(5))
        win.box()
        win.attroff(curses.color_pair(5))
        win.addstr(0, 2, " Menu Principal ", curses.color_pair(5) | curses.A_BOLD)
        
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
        while not SHOULD_QUIT:
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
    global SHOULD_QUIT
    SHOULD_QUIT = True

def main_menu(stdscr):
    menu_items = ["Validar o Ambiente", "Normalizar o Ambiente", "Instalar o Magento", "Sair"]
    current_row = 0
    
    while True:
        height, width = stdscr.getmaxyx()
        win = curses.newwin(height - 2, width - 2, 1, 1)
        
        win.attron(curses.color_pair(5))
        win.box()
        win.attroff(curses.color_pair(5))
        win.addstr(0, 2, " Menu Principal ", curses.color_pair(5) | curses.A_BOLD)
        
        for idx, row in enumerate(menu_items):
            x = 2
            y = 2 + idx
            if idx == current_row:
                win.attron(curses.color_pair(4))
                win.addstr(y, x, row)
                win.attroff(curses.color_pair(4))
            else:
                win.addstr(y, x, row)
        
        win.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                validate_environment(win)
            elif current_row == 1:
                show_message(stdscr, "Normalização", "Normalização do ambiente ainda não implementada.", curses.color_pair(3))
            elif current_row == 2:
                show_message(stdscr, "Instalação", "Instalação do Magento ainda não implementada.", curses.color_pair(3))
            elif current_row == 3:
                break

def main(stdscr):
    # stdscr = init_screen()
    # try:
    #     main_menu(stdscr)
    # finally:
    #     end_screen(stdscr)
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

    menu_items = [
        MenuItem("Validar o Ambiente", validate_environment),
        MenuItem("Normalizar o Ambiente", show_message(stdscr, "Normalização", "Normalização do ambiente ainda não implementada.", 3), 4),
        #MenuItem("Instalar o Magento", show_message(stdscr, "Instalação", "Instalação do Magento ainda não implementada.", 3)),
        MenuItem("Sair", quit_program)
    ]

    menu = Menu(stdscr, menu_items)
    menu.run()

if __name__ == "__main__":
    curses.wrapper(main)
