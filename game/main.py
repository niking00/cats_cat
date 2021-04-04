import os
import random
import keyboard
import time
from collections import deque

TIME_FRAME = 0.05

directory = os.path.abspath(os.curdir)
files = os.listdir(path=directory + "/levels")

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
        self.win = False
        self.scores = 0

    def create_level(self, num_level):
        with open(directory + '/levels/' + str(num_level) + '.txt') as file:
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
        os.system('clear')
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
                'stop': [x, y]}

    def new_list_level_cat(self):
        key = keyboard.read_key()
        time.sleep(0.25)
        x, y = self.cat_position[0], self.cat_position[1]
        while not self.win and not self.kill:
            while key not in DIRECTIONS:
                key = keyboard.read_key()
            object = self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]]
            if object == OBJECTS[0]:
                key = keyboard.read_key()
            elif object == OBJECTS[1]:
                if len(self.mouse_position) == 0:
                    # self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = '0'
                    self.win = True
                else:
                    key = keyboard.read_key()
            elif object == UNITS[0]:
                self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = '30'
            elif object == UNITS[1]:
                self.kill = True
            else:
                break
        if not self.kill and not self.win:
            self.level[x][y] = f' {random.randint(1, 9)} '
            self.scores += int(self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]].strip())
            self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]] = PERSONAGE
        self.check_positions()

    def new_list_level_mouse(self):
        for i in range(0, len(self.mouse_position), 2):
            x, y = self.mouse_position[i], self.mouse_position[i + 1]
            new_position = random.choice(DIRECTIONS)
            object = lambda pos: self.level[self.orientation(x, y)[pos][0]][self.orientation(x, y)[pos][1]]
            while new_position != 'stop':
                if [True for j in DIRECTIONS if object(j) in OBJECTS + [PERSONAGE] + UNITS] == [True] * 4:
                    new_position = 'stop'
                elif object(new_position) in OBJECTS + [PERSONAGE] + UNITS:
                    new_position = random.choice(DIRECTIONS)
                else:
                    break
            self.level[x][y] = f' {random.randint(1, 9)} '
            self.level[self.orientation(x, y)[new_position][0]][self.orientation(x, y)[new_position][1]] = UNITS[0]
            self.new_frame()
            self.check_positions()

    def new_list_level_dog(self):
        for i in range(0, len(self.dog_position), 2):
            x, y = self.dog_position[i], self.dog_position[i + 1]
            graph = Algorithms().matrix_to_graph(self.level)
            start = (x, y)

            try:
                goal = (self.cat_position[0], self.cat_position[1])
                visited = Algorithms().bfs(start, goal, graph)
                way = Algorithms().all_way(start, goal, visited)

                self.level[x][y] = f' {random.randint(1, 9)} '
                if len(way) != 1:
                    self.level[way[-2][0]][way[-2][1]] = UNITS[1]
                else:
                    time.sleep(1)
                    self.level[self.cat_position[0]][self.cat_position[1]] = UNITS[1]
                    self.kill = True
                    break

                self.new_frame()
                self.check_positions()
            except:
                self.check_positions()

    def game(self, num_level):
        self.create_level(num_level)
        while True:
            self.new_frame()
            self.check_positions()
            while self.scores >= 30 and not self.win:
                self.new_list_level_cat()
                if self.win or self.kill:
                    break
                self.scores -= 30
                self.new_frame()
            else:
                self.new_list_level_cat()

            self.new_list_level_mouse()
            self.new_list_level_dog()

            if self.kill:
                self.new_frame()
                time.sleep(1)
                break

            if self.win:
                self.level[self.exit_position[0]][self.exit_position[1]] = PERSONAGE
                self.new_frame()
                break

            self.new_frame()


# TODO:// на перспективу дописать 9 жизней и визуал интерфейс

if __name__ == '__main__':
    os.system('clear')
    print(files)
    for i in range(1, len(files) + 1):
        os.system('clear')
        Game().game(i)
        os.system('clear')
        print('GG')
        time.sleep(5)
