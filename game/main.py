import os
import random
import keyboard
import time
directory = os.path.abspath(os.curdir)
files = os.listdir(path=directory + "\levels")

DICT_OBJECTS = {'#': '███',
           'c': 'cat',
           'm': '(m)',
           'd': 'dog',
           ']': '[ ]'}
OBJECTS = ('███', 'cat', '(m)', 'dog', '[ ]')
DIRECTIONS = ['up', 'right', 'down', 'left']


class Game:
    def __init__(self):
        self.cat_position = []
        self.mouse_position = []
        self.dog_position = []
        self.exit_position = []
        self.level = []
        self.scores = 0

    def create_level(self, num_level):
        with open(directory + '\levels\\' + str(num_level) + '.txt') as file:
            self.level.append([])
            for j in file.read():
                if j in DICT_OBJECTS:
                    self.level[-1].append(DICT_OBJECTS[j])
                elif j == '.':
                    self.level[-1].append(f' {random.randint(1, 9)} ')
                else:
                    self.level.append([])

    def print_level(self):
        for i in self.level:
            for j, q in enumerate(i):
                if j != len(i) - 1:
                    print(q, end='')
                else:
                    print(q)
        print(f'\nТвои очки: {self.scores}')
        print(f'Ты можешь сделать за этот ход {self.scores // 30 + 1} движение')

    def check_positions(self):
        self.mouse_position, self.dog_position = [], []
        for x, i in enumerate(self.level):
            for y, j in enumerate(i):
                if self.level[x][y] == 'cat':
                    self.cat_position = [x, y]
                elif self.level[x][y] == '(m)':
                    self.mouse_position += [x, y]
                elif self.level[x][y] == 'dog':
                    self.dog_position += [x, y]
                elif self.level[x][y] == '[ ]':
                    self.exit_position = [x, y]

    def orientation(self, x, y):
        return {'up': [x - 1, y],
                'right': [x, y + 1],
                'down': [x + 1, y],
                'left': [x, y - 1],
                'stop':  [x, y]}

    def new_list_level_cat(self):
        key = keyboard.read_key()
        time.sleep(0.25)
        x, y = self.cat_position[0], self.cat_position[1]
        if key in self.orientation(x, y):
            while True:
                object = self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]]
                if object in ('███', '[ ]'):
                    if object == '[ ]' and len(self.mouse_position) == 0:
                        self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = ' 0 '
                    else:
                        key = keyboard.read_key()
                elif object == '(m)':
                    self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = '15 '
                else:
                    break
            self.level[x][y] = f' {random.randint(1, 9)} '
            self.scores += int(self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]].strip())
            self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = 'cat'
            self.check_positions()

    def new_list_level_mouse(self):
        for i in range(0, len(self.mouse_position), 2):
            x, y = self.mouse_position[i], self.mouse_position[i+1]
            new_posistion = random.choice(DIRECTIONS)
            object = lambda pos: self.level[self.orientation(x, y)[pos][0]][self.orientation(x, y)[pos][1]]
            while True:
                if [True for j in DIRECTIONS if object(j) in OBJECTS] == [True]*4:
                    new_posistion = 'stop'
                    break
                elif object(new_posistion) in OBJECTS:
                    new_posistion = random.choice(['up', 'right', 'down', 'left'])
                else:
                    break
            self.level[x][y] = f' {random.randint(1, 9)} '
            self.level[self.orientation(x, y)[new_posistion][0]][self.orientation(x, y)[new_posistion][1]] = '(m)'

    def game(self):
        self.create_level(2)
        while True:
            self.print_level()
            self.check_positions()
            if self.scores >= 30 and self.cat_position != self.exit_position:
                self.new_list_level_cat()
                if self.cat_position == self.exit_position:
                    break
                self.scores -= 15
                os.system('cls')
                self.print_level()
                self.new_list_level_cat()
                self.scores -= 15
            else:
                self.new_list_level_cat()
            if self.cat_position == self.exit_position:
                break
            self.new_list_level_mouse()
            os.system('cls')

#TODO:// на перспективу дописать хождение собаки, и чтобы вообще всё красиво, 9 жизней и визуал интерфейс

if __name__ == '__main__':
    os.system('cls')
    Game().game()
    os.system('cls')
    print('GG')
    time.sleep(5)