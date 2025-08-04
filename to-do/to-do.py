import datetime

def setup(filename):
    try:
        open(filename, 'x').close()
    except FileExistsError:
        pass

def prompt(tasks_present):
    if tasks_present:
        lines = [
            '1) Make task',
            '2) Delete existing task',
            '3) Change status of existing task',
            '4) Save and exit'
        ]
        for line in lines:
            print(line)

        while True:
            selection = input('Type the number of your desired choice: ')
            if selection in ['1', '2', '3']:
                return selection
            elif selection == '4':
                return None
            else:
                print('Invalid input!')
    else:
        print('Task list empty!')
        lines = [
            '1) Make task',
            '2) Save and exit'
        ]
        for line in lines:
            print(line)

        while True:
            selection = input('Type the number of your desired choice: ')
            if selection == '1':
                return '1'
            elif selection == '2':
                return None
            else:
                print('Invalid input!')

def make_list(filename):
    task_list = []
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        for line in lines:
            task = {
                'Name': line[4:],
                'Complete': True if line[:3] == '[x]' else False
            }
            task_list.append(task)

    return task_list

def print_tasks(task_list):
    for task in task_list:
        print(f'{'[x]' if task['Complete'] else '[ ]'} {task['Name']}')

def create(task_list):
    while True:
        task_name = input('New task: ').strip()
        if task_name:
            break

    task = {}
    task['Name'] = task_name
    task['Complete'] = False

    task_list.append(task)

def delete(task_list):
    for i, task in enumerate(task_list):
        print(f'{i + 1}) {'[x]' if task['Complete'] else '[ ]'} {task['Name']}')

    while True:
        try:
            del_num = int(input('Type the task number to delete: '))
        except ValueError:
            print('Invalid input! Type a number.')
            continue
        del_num -= 1

        if 0 <= del_num < len(task_list):
            del task_list[del_num]
            break
        else:
            print('Invalid input! Type one in range.')

def change_status(task_list):
        for i, task in enumerate(task_list):
            print(f'{i + 1}) {'[x]' if task['Complete'] else '[ ]'} {task['Name']}')

        while True:
            try:
                statc_num = int(input('Type the task number to change the status of: '))
            except ValueError:
                print('Invalid input! Type a number.')
                continue
            statc_num -= 1

            if 0 <= statc_num < len(task_list):
                task_list[statc_num]['Complete'] = not task_list[statc_num]['Complete']
                break
            else:
                print('Invalid input! Type one in range.')

def save(filename, task_list):
    with open(filename, 'w') as file:
        for task in task_list:
            file.write(f'{'[x]' if task['Complete'] else '[ ]'} {task['Name']}\n')
    
def main():
    filename = f'{datetime.date.today().strftime('%m-%d-%Y')}.txt'
    setup(filename)
    to_do = make_list(filename)

    while True:
        print_tasks(to_do)

        selection = prompt(True if to_do else False)
        if selection == '1':
            create(to_do)
        elif selection == '2':
            delete(to_do)
        elif selection == '3':
            change_status(to_do)
        else:
            save(filename, to_do)
            break

if __name__ == '__main__':
    main()