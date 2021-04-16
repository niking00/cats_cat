import os
import random
import keyboard
import time
import threading
import pyglet
from mutagen.mp3 import MP3
from const import PERSONAGE, UNITS, OBJECTS, DIRECTIONS,\
                  TIME_CLICK, MUSIC, LEVELS, DIRECTORY
from resources import Algorithms
from level import create_level, new_frame

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

    def check_object(self, x, y, pos):
        return self.level[self.orientation(x, y)[pos][0]][self.orientation(x, y)[pos][1]]

    def new_list_level_cat(self):
        key = keyboard.read_key()
        time.sleep(TIME_CLICK)
        x, y = self.cat_position[0], self.cat_position[1]
        while not self.win and not self.kill:
            while key not in DIRECTIONS:
                key = keyboard.read_key()
            object = self.level[self.orientation(x, y)[key][0]][self.orientation(x, y)[key][1]]
            if object == OBJECTS[0]:
                key = keyboard.read_key()
            elif object == OBJECTS[1]:
                if len(self.mouse_position) == 0:
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
            x, y = self.mouse_position[i], self.mouse_position[i+1]
            new_position = random.choice(DIRECTIONS)
            temp = 0
            while new_position != 'stop':
                if [True for j in DIRECTIONS if self.check_object(x, y, j) in OBJECTS + [PERSONAGE] + UNITS] == [True]*4:
                    new_position = 'stop'
                elif self.check_object(x, y, new_position) in OBJECTS + [PERSONAGE] + UNITS:
                    new_position = random.choice(DIRECTIONS)
                else:
                    x1, y1 = self.orientation(x, y)[new_position][0], self.orientation(x, y)[new_position][1]
                    if True in [True for j in DIRECTIONS if self.check_object(x1, y1, j) == PERSONAGE]:
                        if temp < 10:
                            new_position = random.choice(DIRECTIONS)
                            temp += 1
                        else:
                            new_position = 'stop'
                    else:
                        break
            self.level[x][y] = f' {random.randint(1, 9)} '
            self.level[self.orientation(x, y)[new_position][0]][self.orientation(x, y)[new_position][1]] = UNITS[0]
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
                    time.sleep(0.5)
                    self.level[self.cat_position[0]][self.cat_position[1]] = UNITS[1]
                    self.kill = True
                    break
                self.check_positions()
            except:
                self.check_positions()


    def game(self, num_level):
        self.level = create_level(num_level)
        while True:
            new_frame(self.level, self.scores, old_time)
            self.check_positions()
            while self.scores >= 30 and not self.win:
                self.new_list_level_cat()
                if self.win or self.kill:
                    break
                self.scores -= 30
                new_frame(self.level, self.scores, old_time)
            else:
                self.new_list_level_cat()
            self.new_list_level_mouse()
            self.new_list_level_dog()
            if self.kill:
                new_frame(self.level, self.scores, old_time)
                time.sleep(1)
                return False
            if self.win:
                self.level[self.cat_position[0]][self.cat_position[1]] = f' {random.randint(1, 9)} '
                self.level[self.exit_position[0]][self.exit_position[1]] = PERSONAGE
                new_frame(self.level, self.scores, old_time)
                return True

    def play_music(self):
        global song
        global stop_music
        while not stop_music:
            for i in range(1, len(MUSIC)):
                file = DIRECTORY + f'\music\{i}.mp3'
                length_file = MP3(file).info.length
                song = pyglet.media.load(file, streaming=False).play()
                time.sleep(length_file)

    def play(self):
        global song
        global stop_music
        global old_time
        stop_music = False
        player = threading.Thread(target=self.play_music)
        player.start()
        old_time = time.time()
        # for i in range(1, len(LEVELS) + 1):
        for i in range(1, 1 + 1):
            win = False
            while not win:
                os.system('cls')
                win = Game().game(i)
                os.system('cls')
                if win:
                    print('GG')
                else:
                    print('LMAO this is no GG haahahah')
                time.sleep(2)
        stop_music = True
        song.next_source()

        print('Хорошая работа, Але... Ой, а как тебя зовут, юзер?')
        name = input('Моё имя (оно будет зваписано в турнирной таблице) : ')
        os.system('cls')
        print('Отлично, хорошая работа, ' + name + '!',
              'Ваше имя будет увековечено в турнирной таблице!')
        time.sleep(5)








