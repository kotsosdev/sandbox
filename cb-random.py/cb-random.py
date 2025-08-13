from time import sleep
from random import choice
from pyperclip import copy

def get_quotes():
    try:
        with open("quotes.txt", "r") as file:
            content = file.read()
            quotes = content.split("\n")
        return quotes
    
    except FileNotFoundError:
        print("No quotes.text file found - make one and put some quotes in it seperated by newlines.")
        return []

def main():
    quotes = get_quotes()
    try:
        while True:
            copy(choice(quotes))
            sleep(5)
    except KeyboardInterrupt:
        print("Ended!")
    
if __name__ == "__main__":
    main()