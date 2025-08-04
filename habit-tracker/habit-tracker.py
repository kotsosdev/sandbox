import json
from time import sleep
from datetime import datetime
import os

NOW = datetime.now()
DATE = f'{NOW.month}-{NOW.day}-{NOW.year}'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_data():
    try:
        with open('habit-tracker.json', 'r') as file:
            content = file.read()
            if content:
                return json.loads(content)
            else:
                return {}
            
    except FileNotFoundError:
        with open('habit-tracker.json', 'x'): 
            return {}
        
def streak_check(tracker):
    for habit in tracker.values():
        if habit['recent'] != DATE:
            habit['streak'] = 0
        
def prompt(choices, header=None, send_choice=False):
    while True:
        clear_console()
        if header:
            print(f'{header}\n')

        for i, choice in enumerate(choices, start=1):
            print(f'{i}. {choice}')

        try:
            res = int(input('Choice Number: '))
        except ValueError: 
            print('\nPlease enter a integer.')
            sleep(1)
            continue

        if 1 <= res <= i:
            res = res - 1
            return choices[res] if send_choice else res
        else:
            print(f'\nPlease enter a value within 1 and {i}.')
            sleep(1)
            continue
        
def mark_done(tracker):
    if not tracker:
        print('No habits to mark as done!')
        sleep(1)
        return

    choices = [habit.capitalize() for habit in tracker]
    header = 'Mark a habit as done'
    habit = prompt(choices, header, True).lower()
    habit = tracker[habit]

    if habit['recent'] != DATE:
        habit['history'].append(DATE)
        habit['streak'] += 1
    else: 
        print('You already finished this today!')
        sleep(1)

    habit['recent'] = DATE

def view(tracker):
    if not tracker:
        print('No habits to show!')
        sleep(1)
        return

    habits = [habit.capitalize() for habit in tracker]

    for habit in habits:
        name = habit
        habit = tracker[habit.lower()]

        desc = f"""\
{name}
    • Done? {'✓' if habit['recent'] == DATE else '✗'}
    • Streak: {habit['streak']}
    • Recently done: {habit['recent'] if habit['recent'] else 'Never'}
"""
        print(desc)

    input('Press Enter to continue. ')

def add_habit(tracker):
    while True:
        name = input('Habit name: ').strip().lower()

        if not name:
            print('\nEnter at least one valid character')
            sleep(1)
            continue

        if tracker.get(name):
            choices = [
                'Overwrite', 
                'Go back'
            ]
            header = 'This habit is already stored in the tracker.'
            res = prompt(choices, header)

            if res == 1: 
                continue

        tracker[name] = {
            'history': [],
            'streak': 0,
            'recent': None
        }

        break
    
def del_habit(tracker):
    choices = [habit.capitalize() for habit in tracker]
    header = 'Delete a habit - Careful!'
    habit = prompt(choices, header, True).lower()

    del tracker[habit]

def save_data(tracker):
    with open('habit-tracker.json', 'w') as file:
        json.dump(tracker, file)

def menu(data):
    actions = {
        0: mark_done,
        1: view,
        2: add_habit,
        3: del_habit,
        4: save_data
    }

    while True:
        choices = [
            'Mark habit as done',
            'View habits',
            'Add habit',
            'Delete habit',
            'Save and exit'
        ]
        res = prompt(choices)

        clear_console()
        actions[res](data)

        if res == 4: 
            break

def main():
    data = get_data()
    streak_check(data)
    
    try:
        menu(data)
    finally:
        save_data(data)
    
if __name__ == '__main__':
        main()