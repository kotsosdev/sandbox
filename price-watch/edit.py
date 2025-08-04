from utils import clear_console, json_load, json_save
from time import sleep

def prompt(choices, get_choice=False):
    while True:
        clear_console()
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")
        print()

        try:
            response = int(input("Enter an integer: "))
        except ValueError:
            print("\nEnter an integer.")
            sleep(2)
            continue

        if 1 <= response <= i:
            if get_choice: 
                return choices[response - 1]
            else: 
                return response
        else:
            print(f"\nEnter an integer between 1 and {i}")
            sleep(2)

def add(data):
    while True:
        clear_console()
        url = input("Amazon URL: ")

        if "https://www.amazon.com/" not in url:
            print("\nEnter an Amazon link.")
            sleep(2)
            continue
        else:
            break

    clear_console()
    data[url] = {
        "name": input("Product name: "),
        "snapshots": []
    }

    return True

def get_key(data):
    name_to_url = {
        info["name"]: url
        for url, info in data.items()
    }
    choices = [name for name in name_to_url]

    return name_to_url[prompt(choices, True)]

def remove(data):
    if not data:
        print("There is nothing to remove!")
        sleep(2)
        return True

    url = get_key(data)
    del data[url]

    return True

def visualize(data):
    clear_console()
    if not data:
        print("There is nothing to show!\n")

    for url, info in data.items():
        print(f"""\
{url}
    - Name: {info["name"]}
    - Snapshots: {len(info["snapshots"])}
""")

    print("Enter to continue...\n")
    input("")

    return True

def clear_snap(data, url=None):
    if not url:
        url = get_key(data)
    data[url]["snapshots"].clear()
    
    return True

def clear_snaps(data):
    for url in data:
        clear_snap(data, url)

    return True

def wipe_json(data):
    data.clear()

    return True

def clear_data(data):
    if not data:
        print("There is nothing to clear!")
        sleep(2)
        return True
    
    dispatch = {
        1: clear_snap,
        2: clear_snaps,
        3: wipe_json
    }
    choices = [
        "Clear one product's snapshots",
        "Clear all snapshots",
        "Wipe entire json"
    ]
    return dispatch[prompt(choices)](data)

def end(data):
    clear_console()
    if json_save(data):
        print("Success! Enter to continue...")
    else:
        print("Failed! Enter to continue...")
    input("\n")
    clear_console()

    return False

def main():
    data = json_load()
    dispatch = {
        1: add,
        2: remove,
        3: visualize,
        4: clear_data,
        5: end
    }

    running = True
    while running:
        choices = [
            "Add item",
            "Remove item",
            "Visualize json",
            "Clear data",
            "Save and quit"
        ]
        running = dispatch[prompt(choices)](data)

if __name__ == "__main__":
    main()