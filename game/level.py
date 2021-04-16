from colorama import init, Fore, Back
import sys
import random
import os
import time
from const import OBJECTS, UNITS, PERSONAGE, DICT_OBJECTS, TIME_FRAME, DIRECTORY

COLOR_ALL = {OBJECTS[0]: Back.LIGHTBLACK_EX, OBJECTS[1]: Fore.CYAN,
             UNITS[0]: Fore.GREEN, UNITS[1]: Fore.RED,
             PERSONAGE: Fore.LIGHTWHITE_EX,
             'SCORES': Fore.YELLOW}

init()

def create_level(num_level):
    level = []
    with open(DIRECTORY + r'\levels\\' + str(num_level) + '.txt') as file:
        level.append([])
        for j in file.read():
            if j in DICT_OBJECTS:
                level[-1].append(DICT_OBJECTS[j])
            elif j == '.':
                level[-1].append(f' {random.randint(1, 9)} ')
            else:
                level.append([])
    return level


def print_level(level, scores, start_time):
    for i in level:
        for j, q in enumerate(i):
            if j != len(i) - 1:
                if q.strip().isdigit():
                    print(COLOR_ALL['SCORES'] + q + Back.RESET + Fore.RESET, end='')
                else:
                    print(COLOR_ALL[q] + q + Back.RESET + Fore.RESET, end='')
            else:
                print(COLOR_ALL[q] + q + Back.RESET + Fore.RESET)
            sys.stdout.flush()
    print(f'\nТвои очки: {scores}')
    print(f'Ты можешь сделать за этот ход {scores // 30 + 1} движение')
    sec = int(time.time() - start_time)
    print(f'Твоё время {sec // 60} минут {sec - (sec // 60)} секунд')

def new_frame(level, scores, start_time):
    time.sleep(TIME_FRAME)
    os.system('cls')
    print_level(level, scores, start_time)
