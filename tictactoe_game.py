import random
import sys
from typing import List
from string import Template
from collections import namedtuple


# Board = namedtuple('Board', (field for field in 'qweasdzxc'))


def draw_board(current_position: List[int]) -> None:
    values_row = Template('- $value1 | $value2 | $value3 - ')
    _row = '-' * 14
    result = ''
    for i in range(0, 8, 3):
        result += '\n' + _row + '\n'
        result += values_row.substitute(value1=current_position[i],
                                        value2=current_position[i + 1],
                                        value3=current_position[i + 2])
    result += '\n' + _row + '\n'
    print(result)


def start_the_game():
    current_position = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    draw_board(current_position=current_position)
    return current_position


def potential_moves_from(current_situation: List[int]) -> List[int]:
    potential_moves = []
    for value in current_situation:
        if value not in 'XO':
            potential_moves.append(current_situation.index(value) + 1)
    return potential_moves


def random_move(potential_moves: List[int]) -> int:
    return random.choice(potential_moves)


def ai_move(current_situation: List[int], move: int, step_type: str, counter: int) -> List[int]:
    current_situation[move - 1] = step_type
    counter += 1
    draw_board(current_situation)
    return current_situation, counter


def check_win_or_not(current_position: List[int]) -> int:
    win_positions = [
        (1, 4, 7),  ## vertical
        (2, 5, 8),  ## vertical
        (3, 6, 9),  ## vertical

        (1, 2, 3),  ## horizontal
        (4, 5, 6),  ## horizontal
        (7, 8, 9),  ## horizontal

        (1, 5, 9),  ## diagonal
        (3, 5, 7)  ## diagonal
    ]
    x_positions = list((index + 1 for index, value in enumerate(current_position) if value == 'X'))
    o_positions = list((index + 1 for index, value in enumerate(current_position) if value == 'O'))
    print(f'X = {x_positions}')
    print(f'O = {o_positions}')
    for each in win_positions:
        if find_subarray(x_positions, each):
            print('X wins!!')
            return 1
        if find_subarray(o_positions, each):
            print('O wins!!')
            return 1
    print("! Игра все ещё продолжается !  ")
    return 0


def make_the_move(values: List[int], step_type: str, counter: int):
    index = input(f'Куда поставим "{step_type}" ? Введите индекс от 1 до 9 :')
    try:
        index = int(index)
    except ValueError:
        print('\nYou did not enter a valid integer')
    while index not in potential_moves_from(values):
        index = int(input(f'Куда поставим "{step_type}" ? Введите индекс от 1 до 9 :'))
    if values[index - 1] in 'XO':
        draw_board(values)
        print('Там же занято ! НУ посмотри внимательнее !')
        return values, counter
    values[index - 1] = step_type
    counter += 1
    draw_board(values)
    return values, counter


def find_subarray(first_arr: List[int], second_arr: List[int]) -> bool:
    first_ptr = 0
    second_ptr = 0

    first_arr_len = len(first_arr)
    second_arr_len = len(second_arr)

    while first_ptr < first_arr_len and second_ptr < second_arr_len:
        if first_arr[first_ptr] == second_arr[second_ptr]:
            first_ptr += 1
            second_ptr += 1

            if second_ptr == second_arr_len:
                return True

        else:
            first_ptr = first_ptr - second_ptr + 1
            second_ptr = 0

    return False


def min_max(current_position: List[int], depth: int) -> int:
    evaluation = {}
    if check_win_or_not(current_position):
        return 10 - depth
    for step in potential_moves_from(current_position):
        current_position[step - 1] = 'O'
        upd_position = current_position
        evaluation[step] = min_max(upd_position, depth=depth + 1)
    print(evaluation)


if __name__ == '__main__':
    current_position = start_the_game()
    counter_moves = 0

    while not check_win_or_not(current_position):
        print(f'Potential moves : {potential_moves_from(current_position)}')
        if not potential_moves_from(current_position):
            print('!! НИЧЬЯ !!')
            break
        if counter_moves % 2 == 1:
            current_position, counter_moves = make_the_move(current_position, 'X', counter_moves)
        else:
            move = random_move(potential_moves_from(current_position))
            current_position, counter_moves = ai_move(current_position, move, 'O', counter_moves)
        if counter_moves == 4:
            min_max(current_position, 0)
