import subprocess
import re
import curses
from modules.curses.Menu import Menu
from modules.curses.MenuItem import MenuItem
#from utils.system import config

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

def validate_environment(stdscr):
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

        message = f"{icon}" # {service.upper()} {config.LANGUAGE_STRINGS["INSTALLED"] if status else config.LANGUAGE_STRINGS["NOT_INSTALLED"]} - {result.strip()}"
        results.append((message, color))
    
    items = [MenuItem(message, lambda win: None, color) for message, color in results]
    #additional_buttons = [MenuItem(config.LANGUAGE_STRINGS["BTN_RETURN_TO_MENU"])]#], main)]
    Menu(stdscr, "TITLE_VALIDATE_ENVIRONMENT", "TITLE_VALIDATE_ENVIRONMENT", items, items).run()