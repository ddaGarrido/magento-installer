import curses
import inspect
from utils.system import config
from utils.system.config import get_language_string

from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:   # noinspection PyCompatibility,PyProtectedMember
    from _curses import window
    from typing import Callable

    Window = window
    #from cursesmenu.items.menu_item import MenuItem
else:
    Window = Any
    MenuItem = Any

class Menu:

    #currently_active_menu: CursesMenu | None = None
    stdscr: Window | None = None

    def __init__(self, stdscr, title, subtitle, items, footer_items, show_exit_btn=True):
        self.stdscr = stdscr
        self.title = get_language_string(title)
        self.subtitle = get_language_string(subtitle)
        self.items = items
        self.footer_items = footer_items
        self.show_exit_btn = show_exit_btn

        self.screen = Window | None

        self.highlight: int = curses.A_BOLD
        self.normal: int = curses.A_NORMAL
        self.current_row = 0

        #if show_exit_btn:
            #self.end_items.append(MenuItem("Exit", self.exit))

    # def add_item(self, item):
    #     self.items.append(item)

    # def add_footer_item(self, item):
    #     self.footer_items.append(item)

    # def handle_input(self, key):
    #     pass

    # def clear(self):
    #     self.screen.clear()

    def display_clean(self):
        self.stdscr.clear()
        self.display()

    def run(self):
        self.display_clean()
        while not config.SHOULD_QUIT:
            self.handle_input()
            self.display()

    def handle_input(self):
        key = self.stdscr.getch()

        if key == curses.KEY_UP and self.current_row > 0:
            self.current_row -= 1
        elif key == curses.KEY_DOWN and self.current_row < len(self.items) - 1: #+ len(self.additional_buttons) - 1:
            self.current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if self.current_row < len(self.items):
                action_method = self.items[self.current_row].action
                sig = inspect.signature(action_method)
                if len(sig.parameters) == 1:
                    action_method(self.stdscr)
                else:
                    action_method()
            #else:
                #self.additional_buttons[self.current_row - len(self.items)].action(self.stdscr)

    def mount_items(self):
        for idx, item in enumerate(self.items):
            x = 2
            y = 2 + idx
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(4))
                self.stdscr.addstr(y, x, item.text)
                self.stdscr.attroff(curses.color_pair(4))
            else:
                self.stdscr.addstr(y, x, item.text)

    def get_center_pos(self, text):
        height, width = self.stdscr.getmaxyx()
        x_pos = (width // 2) - (len(text) // 2)
        return x_pos

    def display_window(self, color_pair):
        self.stdscr.attron(color_pair)
        self.stdscr.box()
        self.stdscr.attroff(color_pair)

    def set_window_title(self, color_pair):
        x_pos = self.get_center_pos(self.title)
        title = " " + self.title + " "
        self.stdscr.addstr(0, x_pos, title, color_pair | curses.A_BOLD)

    def start_display(self):
        self.display_window(curses.color_pair(5))
        self.set_window_title(curses.color_pair(5))

    def display(self):
        self.start_display()

        self.mount_items()

        # for idx, button in enumerate(self.end_items):
        #     x = 2
        #     y = height - len(self.end_items) + idx - 2
        #     if len(self.items) + idx == self.current_row:
        #         self.stdscr.attron(curses.color_pair(4))
        #         self.stdscr.addstr(y, x, button)
        #         self.stdscr.attroff(curses.color_pair(4))
        #     else:
        #         self.stdscr.addstr(y, x, button)
        
        self.stdscr.refresh()

    # def render(self):
    #     self.clear()
    #     # Renderiza título e subtítulo
    #     self.screen.addstr(1, 2, self.title, curses.color_pair(1))
    #     self.screen.addstr(2, 2, self.subtitle, curses.color_pair(2))
        
    #     # Renderiza itens do menu
    #     for index, item in enumerate(self.items):
    #         item.render(index == 0)  # Seleciona o primeiro item como exemplo

    #     # Renderiza itens do rodapé
    #     for index, item in enumerate(self.footer_items):
    #         item.render(False)  # Footer items não são selecionáveis neste exemplo

    #     self.screen.refresh()

# class MenuItem:
#     def __init__(self, name, action=None, item_type="standard"):
#         self.name = name
#         self.action = action
#         self.item_type = item_type

#     def select(self):
#         if self.action:
#             self.action()

#     def render(self, selected):
#         # Exemplo de renderização básica
#         display_name = f"> {self.name}" if selected else f"  {self.name}"
#         # Adiciona mais lógica para diferenciar entre tipos de item, etc.

# class MenuButton(MenuItem):
#     def __init__(self, name, action, shortcut):
#         super().__init__(name, action, item_type="button")
#         self.shortcut = shortcut

#     def render(self, selected):
#         display_name = f"[{self.shortcut}] {self.name}" if selected else f" {self.name}"
#         # Adiciona a renderização customizada para botões


# def main(stdscr):

#     menu = Menu("Main Menu", "Select an option:")
#     menu.add_item(MenuItem("Option 1", lambda: print("Option 1 selected")))
#     menu.add_item(MenuItem("Option 2", lambda: print("Option 2 selected")))
#     menu.add_item(MenuItem("Option 3", lambda: print("Option 3 selected")))
#     menu.add_footer_item(MenuButton("Exit", lambda: print("Exit selected"), "X"))

#     menu.screen = stdscr
#     menu.render()

#     while True:
#         key = stdscr.getch()
#         if key == ord('q'):
#             break
#         menu.handle_input(key)

# if __name__ == "__main__":
#     curses.wrapper(main)