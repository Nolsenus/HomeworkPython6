import random


def print_grid(grid):
    for i in range(3):
        print(' | '.join(grid[3 * i:3 * (i + 1)]))


def get_possible_win(grid, symbol):
    are_symbol = [False] * 3
    # Строки
    for i in range(3):
        for j in range(3):
            are_symbol[j] = grid[3 * i + j] == symbol
        if are_symbol[0] and are_symbol[1]:
            if grid[3 * i + 2] == '-':
                return 3 * i + 2
        if are_symbol[0] and are_symbol[2]:
            if grid[3 * i + 1] == '-':
                return 3 * i + 1
        if are_symbol[1] and are_symbol[2]:
            if grid[3 * i] == '-':
                return 3 * i
    # Столбцы
    for i in range(3):
        for j in range(3):
            are_symbol[j] = grid[i + 3 * j] == symbol
        if are_symbol[0] and are_symbol[1]:
            if grid[i + 6] == '-':
                return i + 6
        if are_symbol[0] and are_symbol[2]:
            if grid[i + 3] == '-':
                return i + 3
        if are_symbol[1] and are_symbol[2]:
            if grid[i] == '-':
                return i
    # Диагонали
    for i in range(3):
        are_symbol[i] = grid[i * 4] == symbol
    if are_symbol[0] and are_symbol[1]:
        if grid[8] == '-':
            return 8
    if are_symbol[0] and are_symbol[2]:
        if grid[4] == '-':
            return 4
    if are_symbol[1] and are_symbol[2]:
        if grid[0] == '-':
            return 0
    for i in range(1, 4):
        are_symbol[i - 1] = grid[i * 2] == symbol
    if are_symbol[0] and are_symbol[1]:
        if grid[6] == '-':
            return 6
    if are_symbol[0] and are_symbol[2]:
        if grid[4] == '-':
            return 4
    if are_symbol[1] and are_symbol[2]:
        if grid[2] == '-':
            return 2
    return False


def count_doubles(grid, symbol):
    count = 0
    # Строки
    for i in range(3):
        row = grid[3 * i:3 * (i + 1)]
        if row.count(symbol) == 2 and '-' in row:
            count += 1
    # Столбцы
    for i in range(3):
        column = grid[i::3]
        if column.count(symbol) == 2 and '-' in column:
            count += 1
    diag = grid[::4]
    if diag.count(symbol) == 2 and '-' in diag:
        count += 1
    diag = grid[2:7:2]
    if diag.count(symbol) == 2 and '-' in diag:
        count += 1
    return count


def get_possible_fork(grid, symbol):
    for spot in filter(lambda x: grid[x] == '-', range(len(grid))):
        grid[spot] = symbol
        doubles_count = count_doubles(grid, symbol)
        grid[spot] = '-'
        if doubles_count > 1:
            fork = spot
            return fork
    return False


def check_corners(grid, symbol):
    opposing_symbol = 'X' if symbol == 'O' else 'O'
    for i in [0, 2]:
        if grid[i] == opposing_symbol and grid[8 - i] == '-':
            return 8 - i
        if grid[8 - i] == opposing_symbol and grid[i] == '-':
            return i
    return False


def get_empty_corner(grid):
    for i in [0, 2, 6, 8]:
        if grid[i] == '-':
            return i
    return False


def get_empty_middle_of_side(grid):
    for i in [1, 3, 5, 7]:
        if grid[i] == '-':
            return i
    return False


def smart_move(grid, symbol):
    possible_win = get_possible_win(grid, symbol)
    if possible_win:
        grid[possible_win] = symbol
        return
    possible_loss = get_possible_win(grid, 'X' if symbol == 'O' else 'O')
    if possible_loss:
        grid[possible_loss] = symbol
        return
    possible_fork = get_possible_fork(grid, symbol)
    if possible_fork:
        grid[possible_fork] = symbol
        return
    possible_fork_against = get_possible_fork(grid, 'X' if symbol == 'O' else 'O')
    if possible_fork_against:
        grid[possible_fork_against] = symbol
        return
    if grid[4] == '-':
        grid[4] = symbol
        return
    opposing_corner = check_corners(grid, symbol)
    if opposing_corner:
        grid[opposing_corner] = symbol
        return
    empty_corner = get_empty_corner(grid)
    if empty_corner is not False:
        grid[empty_corner] = symbol
        return
    grid[get_empty_middle_of_side(grid)] = symbol


def random_move(grid, symbol):
    blanks = list(filter(lambda x: grid[x] == '-', range(len(grid))))
    random_blank = random.choice(blanks)
    grid[random_blank] = symbol


def player_move(grid, symbol):
    is_valid_turn = False
    print('Ваш ход.')
    while not is_valid_turn:
        try:
            row = int(input('Введите номер строки (нумерация идёт сверху вниз, начиная с 0): '))
            if row < 0 or row > 2:
                print('Номером строки может быть только 0, 1 или 2.')
                continue
        except ValueError:
            print('Необходимо ввести одну цифру (0, 1 или 2).')
            continue
        try:
            column = int(input('Введите номер столбца (нумерация идёт слева направо, начиная с 0): '))
            if column < 0 or column > 2:
                print('Номером столбца может быть только 0, 1 или 2.')
                continue
        except ValueError:
            print('Необходимо ввести одну цифру (0, 1 или 2).')
            continue
        pos = 3 * row + column
        if grid[pos] == '-':
            is_valid_turn = True
            grid[pos] = symbol
        else:
            print(f'На этомм месте уже стоит {grid[pos]}.')


def check_win(grid, symbol):
    # Строки
    is_win = True
    for i in range(3):
        for j in range(3):
            is_win = is_win and grid[3 * i + j] == symbol
        if is_win:
            return True
        is_win = True
    # Столбцы
    for i in range(3):
        for j in range(3):
            is_win = is_win and grid[i + 3 * j] == symbol
        if is_win:
            return True
        is_win = True
    # Диагонали
    for i in range(3):
        is_win = is_win and grid[4 * i] == symbol
    if is_win:
        return True
    is_win = True
    for i in range(1, 4):
        is_win = is_win and grid[2 * i] == symbol
    return is_win


def main():
    is_players_move = random.choice([True, False])
    grid = ['-'] * 9
    is_bot_smart = input('Вы хотите иметь шанс победить? (Нет/что-либо кроме нет): ').lower() == 'нет'
    symbol = 'X'
    print_grid(grid)
    winner_determined = False
    while True:
        if is_players_move:
            player_move(grid, symbol)
        elif is_bot_smart:
            smart_move(grid, symbol)
            print('Бот сделал умный ход:')
        else:
            random_move(grid, symbol)
            print('Бот сделал случайный ход:')
        print_grid(grid)
        winner_determined = check_win(grid, symbol)
        if winner_determined or '-' not in grid:
            break
        is_players_move = not is_players_move
        if symbol == 'X':
            symbol = 'O'
        else:
            symbol = 'X'
    if winner_determined:
        if is_players_move:
            print(f'Вы победили, играя за {symbol}.')
        else:
            print(f'Бот победил, играя за {symbol}')
    else:
        print('Ничья.')


if __name__ == '__main__':
    main()
