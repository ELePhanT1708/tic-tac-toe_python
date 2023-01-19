#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

MINIMAX_LAUNCHES = 0


def evaluate(state, depth):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +10 - depth * 1
    elif wins(state, HUMAN):
        score = -10 + depth * 1
    else:
        score = 0

    return score ##


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],

        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],

        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, potential_moves, player, depth):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param potential_moves: node index in the tree (0 <= potential_moves <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    global MINIMAX_LAUNCHES
    MINIMAX_LAUNCHES += 1
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if potential_moves == 0 or game_over(state):
        score = evaluate(state, depth)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, potential_moves - 1, -player, depth + 1)
        print(score[2])
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    Очистить консоль
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Выводит состояние полей
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    Вызывает функцию МинМакс если глубина < 9,
    Иначе выбирает случайно поле из возможных.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    potential_moves = len(empty_cells(board))
    if potential_moves == 0 or game_over(board):
        return

    clean()
    print(f'Ход алгоритма: [{c_choice}]')
    render(board, c_choice, h_choice)

    if potential_moves > 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, potential_moves, COMP, 0)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    Ход человека
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    potential_moves = len(empty_cells(board))
    if potential_moves == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Ваш ход :[{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Число из (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Плохой ход')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Конец игры ')
            exit()
        except (KeyError, ValueError):
            print('Введите число !')


def main():
    """
    Логика игры
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Выбери X или O\nВыбрано: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Конец игры')
            exit()
        except (KeyError, ValueError):
            print('Введите число !')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may start first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('Хотите начать?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Конец игры')
            exit()
        except (KeyError, ValueError):
            print('Введите число !')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''
        # ai_turn(h_choice, c_choice)
        human_turn(c_choice, h_choice)

        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'Ваш ход [{h_choice}]')
        render(board, c_choice, h_choice)
        print('Вы ВЫИГРАЛИ !')
    elif wins(board, COMP):
        clean()
        print(f'Ход алгоритма [{c_choice}]')
        render(board, c_choice, h_choice)
        print('Вы ПРОИГРАЛИ !')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('НИЧЬЯ!')
    print(MINIMAX_LAUNCHES)
    exit()


if __name__ == '__main__':
    main()
