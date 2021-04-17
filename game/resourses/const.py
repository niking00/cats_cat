import os

TIME_FRAME = 0
TIME_CLICK = 0.1

DICT_OBJECTS = {'#': '   ',
                'c': 'cat',
                'm': '(m)',
                'd': 'dog',
                ']': '[ ]'}

DIRECTIONS = ['up', 'right', 'down', 'left']
OBJECTS = ['   ', '[ ]']
UNITS = ['(m)', 'dog']
PERSONAGE = 'cat'

DIRECTORY = os.path.abspath(os.curdir)
LEVELS = os.listdir(path=DIRECTORY + "\levels")
MUSIC = os.listdir(path=DIRECTORY + "\music")