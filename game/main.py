import os
import random
import keyboard
import time
from collections import deque

TIME_FRAME = 0.05

directory = os.path.abspath(os.curdir)
files = os.listdir(path=directory + "\levels")

DICT_OBJECTS = {'#': '███',
                'c': 'cat',
                'm': '(m)',
                'd': 'dog',
                ']': '[ ]'}
OBJECTS = ['███', '[ ]']
UNITS = ['(m)', 'dog']
PERSONAGE = 'cat'
DIRECTIONS = ['up', 'right', 'down', 'left']

class Algorithms():
    def matrix_to_graph(self, matrix):
        graph = {}
        ways = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for y, i in enumerate(matrix):
            for x, j in enumerate(i):
                if matrix[x][y] not in OBJECTS + [UNITS[0]]:
                    graph[(x, y)] = []
                    for way in ways:
                        if matrix[x + way[0]][y + way[1]] not in OBJECTS + UNITS:
                            graph[(x, y)].append((x + way[0], y + way[1]))
        return graph

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def all_way(self, start, goal, visited):
        cur_node = goal
        way = []
        while cur_node != start:
            cur_node = visited[cur_node]
            way.append(cur_node)
        return way

class Game:
    def __init__(self):
        self.cat_position = []
        self.mouse_position = []
        self.dog_position = []
        self.exit_position = []
        self.level = []
        self.kill = False
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

    def new_frame(self):
        time.sleep(TIME_FRAME)
        os.system('cls')
        self.print_level()

    def check_positions(self):
        self.mouse_position, self.dog_position = [], []
        for x, i in enumerate(self.level):
            for y, j in enumerate(i):
                if self.level[x][y] == PERSONAGE:
                    self.cat_position = [x, y]
                elif self.level[x][y] == UNITS[0]:
                    self.mouse_position += [x, y]
                elif self.level[x][y] == UNITS[1]:
                    self.dog_position += [x, y]
                elif self.level[x][y] == OBJECTS[1]:
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
        while key not in DIRECTIONS:
            key = keyboard.read_key()
        while True:
            object = self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]]
            if object in OBJECTS + [UNITS[1]]:
                if object == OBJECTS[1] and len(self.mouse_position) == 0:
                    self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = ' 0 '
                else:
                    key = keyboard.read_key()
            elif object == UNITS[0]:
                self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = '20 '
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
                if [True for j in DIRECTIONS if object(j) in OBJECTS + [PERSONAGE] + UNITS] == [True]*4:
                    new_posistion = 'stop'
                    break
                elif object(new_posistion) in OBJECTS + [PERSONAGE] + UNITS:
                    new_posistion = random.choice(DIRECTIONS)
                else:
                    break
            self.level[x][y] = f' {random.randint(1, 9)} '
            self.level[self.orientation(x, y)[new_posistion][0]][self.orientation(x, y)[new_posistion][1]] = UNITS[0]
            self.new_frame()

    def new_list_level_dog(self):
        for i in range(0, len(self.dog_position), 2):
            x, y = self.dog_position[i], self.dog_position[i + 1]
            graph = Algorithms().matrix_to_graph(self.level)
            start = (x, y)
            goal = (self.cat_position[0], self.cat_position[1])
            try:
                visited = Algorithms().bfs(start, goal, graph)
                way = Algorithms().all_way(start, goal, visited)
                self.level[x][y] = f' {random.randint(1, 9)} '
                if len(way) != 1:
                    self.level[way[-2][0]][way[-2][1]] = UNITS[1]
                else:
                    self.level[way[-1][0]][way[-1][1]] = UNITS[1]
                    self.kill = True
            except:
                pass
            self.new_frame()


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
            self.new_list_level_dog()

            if self.kill:
                self.new_frame()
                self.check_positions()
                self.level[self.dog_position[0]][self.dog_position[1]] = f' {random.randint(1, 9)} '
                self.level[self.cat_position[0]][self.cat_position[1]] = UNITS[1]
                self.new_frame()
                time.sleep(1)
                break

            os.system('cls')

#TODO:// на перспективу дописать 9 жизней и визуал интерфейс

if __name__ == '__main__':
    os.system('cls')
    Game().game()
    os.system('cls')
    print('GG')
    time.sleep(5)