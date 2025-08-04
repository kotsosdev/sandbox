import os
import time
import random

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def intro():
    clear_console()
    print('Welcome to minesweeper!')
    input('Press ENTER to start!')
    clear_console()

def get_board_dimensions():
    difficulty = {
        'easy': 10,
        'medium': 18,
        'hard': 24
    }
    while True:
        lines = [
            'Select your difficulty...',
            'Easy -> 10x10',
            'Medium -> 18x18',
            'Hard -> 24x24',
            ''
        ]
        for line in lines:
            print(line)

        res = input("Type your choice: ").lower().strip()
        if res in difficulty:
            clear_console()
            return difficulty[res]
        else:
            print('Invalid input!')
            time.sleep(2)
            clear_console()

def get_boards(dimensions=0):
    if not dimensions:
        dimensions = get_board_dimensions()
    return [['■' for _ in range(dimensions)] for _ in range(dimensions)], [[0 for _ in range(dimensions)] for _ in range(dimensions)]

def print_board(board, withcoords=False):
    if withcoords:
        for i, row in enumerate(board):
            print(f'{abs(i - len(board)):2} {" ".join(f"{cell:2}" for cell in row)}')
        print('  ' + ' '.join(f'{i + 1:2}' for i in range(len(board))))
    else:
        for row in board:
            print('  '.join(row))

def get_neighbors(row, column, dimensions):
    neighbors = []
    offset = [-1, 0, 1]
    for r_offset in offset:
        for c_offset in offset:
            if r_offset == 0 and c_offset == 0:
                continue
            n_row = row + r_offset
            n_column = column + c_offset
            if 0 <= n_row < dimensions and 0 <= n_column < dimensions:
                neighbors.append((n_row, n_column))
    return neighbors

def lay_all_bombs(board, avoid=None):
    if len(board) == 10:
        bombs = 10
    elif len(board) == 18:
        bombs = 40
    elif len(board) == 24:
        bombs = 99
    else:
        return None

    while bombs > 0:
        place_bomb(board, avoid)
        bombs -= 1
    return board

def reveal(row, column, frontend, backend):
    f_cell = frontend[row][column]
    b_cell = backend[row][column]
    if not (0 <= row < len(frontend) and 0 <= column < len(frontend[0])):
        return
    if f_cell == '⚑':
        return 'Flag'
    if f_cell != '■':
        return
    if b_cell == -1:
        return 'Bomb'
    b_cell = backend[row][column]
    frontend[row][column] = '□' if b_cell == 0 else str(b_cell)
    if b_cell == 0:
        neighbors = get_neighbors(row, column, len(frontend))
        for n_row, n_column in neighbors:
            reveal(n_row, n_column, frontend, backend)

def place_bomb(board, avoid=None):
    while True:
        row, column = random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)
        if board[row][column] != -1 and (row, column) != avoid:
            break
    board[row][column] = -1
    neighbors = get_neighbors(row, column, len(board))
    for n_row, n_column in neighbors:
        if board[n_row][n_column] != -1:
            board[n_row][n_column] += 1

def safe_reveal(row, column, frontend, backend):
    while True:
        if backend[row][column] != 0:
            frontend, backend = get_boards(len(frontend))
            lay_all_bombs(backend, (row, column))
            continue
        reveal(row, column, frontend, backend)
        return frontend, backend

def selection(frontend, dimensions, tip=False):
    while True:
        clear_console()
        print_board(frontend, True)
        if tip:
            lines = [
                '',
                'Format input as "x y (optional, to place or remove a flag: f)"',
                'Ex: 3 5 or 3 5 f',
                '',
                '*Place an "f" at the end of your input to flag instead of dig',
                ''
            ]
            for line in lines:
                print(line)
        res = input().strip().lower().split()
        if 2 <= len(res) <= 3:
            try:
                for i in range(0, 2):
                    res[i] = int(res[i])
            except (ValueError, TypeError):
                print('Invalid input!')
                time.sleep(2)
                continue
            if not (1 <= res[0] <= dimensions and 1 <= res[1] <= dimensions):
                print('Coordinates out of range!')
                time.sleep(2)
                continue
            if len(res) == 3:
                if res[2] == 'f':
                    return res[0], res[1], True
                else:
                    print('Invalid input!')
                    time.sleep(2)
                    continue
            else:
                return res[0], res[1], False
        print('Invalid input!')
        time.sleep(2)

def rects_to_indices(x, y, dimensions):
    row, column = dimensions - y, x - 1
    return row, column

def indices_to_rects(row, column, dimensions):
    x, y = column + 1, dimensions - row
    return x, y

def reveal_frontend(loserrow, losercolumn, frontend, backend, dimensions, won):
    clear_console()
    for row in range(dimensions):
        for column in range(dimensions):
            f_cell = frontend[row][column]
            b_cell = backend[row][column]
            if b_cell == -1:
                frontend[row][column] = 'B'
            elif b_cell != -1 and f_cell == '⚑':
                frontend[row][column] = 'X'
            if row == loserrow and column == losercolumn and not won:
                frontend[row][column] = '@'

def handle_flag(row, column, frontend):
    f_cell = frontend[row][column]
    if f_cell == '⚑':
        frontend[row][column] = '■'
    elif f_cell == '■':
        frontend[row][column] = '⚑'
    if f_cell == '□':
        print('That space is already dug!')
        time.sleep(2)

def victory(frontend, backend, dimensions):
    for row in range(dimensions):
        for column in range(dimensions):
            if frontend[row][column] == '■' and backend[row][column] != -1:
                return False
    return True

def main():
    intro()
    frontend, backend = get_boards()
    dimensions = len(frontend)
    backend = lay_all_bombs(backend)
    roundnum = 0
    won = False
    while True:
        if roundnum <= 3:
            x, y, flag = selection(frontend, dimensions, True)
        else:
            x, y, flag = selection(frontend, dimensions, False)
        row, column = rects_to_indices(x, y, dimensions)
        if roundnum == 0:
            frontend, backend = safe_reveal(row, column, frontend, backend)
        elif flag:
            handle_flag(row, column, frontend)
        elif not flag:
            dug = reveal(row, column, frontend, backend)
            if dug == 'Bomb':
                won = False
                break
            elif dug == 'Flag':
                print('Take out the flag first.')
                time.sleep(2)
                continue
            else:
                won = victory(frontend, backend, dimensions)
                if won:
                    break
        roundnum += 1
    reveal_frontend(row, column, frontend, backend, dimensions, won)
    print_board(frontend)
    if won:
        print('\nWINNER!!!!')
    else:
        print('\nGAME OVER!')
    time.sleep(5)

if __name__ == "__main__":
    main()