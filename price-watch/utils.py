import os
import json
from datetime import datetime

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def timestamp():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def log(message):
    with open("debug.log", "a") as file:
        file.write(f"[{timestamp()}] {message}\n")

def json_load():
    try:
        with open("prices.json", "r") as file:
            return json.load(file)
        
    except (FileNotFoundError, json.JSONDecodeError):
        with open("prices.json", "w") as file:
            file.write("{}")
        return {}
    
def json_save(data):
    try: 
        json_str = json.dumps(data, indent=4)
        with open("prices.json", "w") as file:
            file.write(json_str)
        return True

    except TypeError:
        return False