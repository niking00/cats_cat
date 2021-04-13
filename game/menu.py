import os
import time
import keyboard
import math
from resources_game import Game
from const import DIRECTORY
import pyglet
from mutagen.mp3 import MP3
import threading

DIRECTIONS = {'up': -1, 'down': 1, 'enter': ''}

class Menu:
    def __init__(self):
        self.menu = self.readline_menu()
        self.key = ''
        self.start_menu = self.menu[:6]
        self.middle_menu = self.menu[6:16]
        self.end_menu = self.menu[16:]
        self.cursor = '{=>'
        self.len_button = math.ceil(len(self.middle_menu) / 4) + 1
        self.cursor_position = 0
        self.start_game = 0
        self.records = 1
        self.about_the_game = 2
        self.team = 3

        self.exit = False

    def readline_menu(self):
        with open('menu.txt', encoding="utf-8") as f:
            arr = [[]]
            for i in f.read():
                if i != '\n':
                    arr[-1].append(i)
                else:
                    arr.append([])
        return arr

    def print_menu(self):
        for i in self.start_menu + self.middle_menu + self.end_menu:
            print(''.join(i))

    def move_menu(self):
        self.key = keyboard.read_key()
        time.sleep(0.3)
        while self.key not in DIRECTIONS:
            self.key = keyboard.read_key()

        if self.key != 'enter':
            temp = 0
            for i in self.middle_menu[(self.cursor_position % self.len_button) * 3]:
                if i == self.cursor[0]:
                    for j in range(len(self.cursor)):
                        self.middle_menu[(self.cursor_position % self.len_button) * 3][temp + j] = ' '
                    break
                else:
                    temp += 1
            self.cursor_position += DIRECTIONS[self.key]
            for i in range(len(self.cursor)):
                self.middle_menu[(self.cursor_position % self.len_button) * 3][temp + i] = self.cursor[i]

    def check_menu(self):
        global song
        global stop_music
        stop_music = False
        threading.Thread(target=self.play_music).start()
        while True:
            self.print_menu()
            self.move_menu()
            if self.key == 'enter':
                pos = abs(self.cursor_position % self.len_button)

                if pos == self.start_game:
                    stop_music = True
                    song.next_source()
                    Game().play()
                    os.system('cls')
                    break
                elif pos == self.records:
                    os.system('cls')
                    print('пока здесь ничего нет но обязательно будет')
                    time.sleep(2)
                elif pos == self.about_the_game:
                    os.system('cls')
                    print('пока здесь ничего нет но обязательно будет')
                    time.sleep(2)
                elif pos == self.team:
                    os.system('cls')
                    print('пока здесь ничего нет но обязательно будет')
                    time.sleep(2)

            os.system('cls')

    def play_music(self):
        global song
        global stop_music
        while not stop_music:
            file = DIRECTORY + f'\music\menu.mp3'
            length_file = MP3(file).info.length
            song = pyglet.media.load(file, streaming=False).play()
            time.sleep(length_file)

while True:
    Menu().check_menu()



