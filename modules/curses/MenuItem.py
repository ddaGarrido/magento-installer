#import curses
#from utils.system import config
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

class MenuItem:
    def __init__(self, text, action=None, item_type="standard"):
        self.text = get_language_string(text)
        self.action = action
        self.item_type = item_type

    def select(self):
        if self.action:
            self.action()

    def render(self, selected):
        # Exemplo de renderização básica
        display_name = f"> {self.text}" if selected else f"  {self.text}"
        # Adiciona mais lógica para diferenciar entre tipos de item, etc.

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