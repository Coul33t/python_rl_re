from player import *
from game_map import *

import tdl

CONSOLE_WIDTH = 90
CONSOLE_HEIGHT = 50

MESSAGE_WIDTH = CONSOLE_WIDTH
MESSAGE_HEIGHT = 12

DUNGEON_DISPLAY_WIDTH = 60
DUNGEON_DISPLAY_HEIGHT = CONSOLE_HEIGHT-MESSAGE_HEIGHT

PANEL_WIDTH = CONSOLE_WIDTH - DUNGEON_DISPLAY_WIDTH
PANEL_HEIGHT = CONSOLE_HEIGHT - MESSAGE_HEIGHT

MAP_WIDTH = 200
MAP_HEIGHT = 200

MOVEMENT_KEYS = {'KP5': [0, 0], 'KP2': [0, 1], 'KP1': [-1, 1], 'KP4': [-1, 0], 'KP7': [-1, -1], 'KP8': [0, -1], 'KP9': [1, -1], 'KP6': [1, 0], 'KP3': [1, 1]}


class Engine:
    def __init__(self):
        tdl.set_font('fonts/Kelora_16x16_diagonal.png')
        self._main_console = tdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT)

        self._map_console = tdl.init(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT)

        self._width = width
        self._height = height

        self._game_map = GameMap(width, height)
        self._fov_map = tdl.map.Map(width, height)
        self._fov_recompute = True

        self._entities = []
        
        self._game_state = 'main_menu'

        self._player = Player(0, 0, '@')
        self._player_action = 'didnt_take_turn'

        


    def handling_keys(self):
        user_input = None

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event

        if user_input:
            if user_input.key == 'ESCAPE':
                return 'exit'

            if self._game_state == 'playing':

                if user_input.key in MOVEMENT_KEYS:
                    print('Motion !')

                else:
                    return 'didnt_take_turn'

        else:
            return 'didnt_take_turn'




    def is_blocked(self, x, y):
        if self._game_map.is_blocked(x, y):
            return True

        for entity in self._entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return True




    def move_cost(self, x, y):
        if self._game_map.is_blocked(x, y):
            return 0
        else:
            for entity in entities:
                if entity.blocks and entity.x == x and entity.y == y:
                    return 10

        return 1



    def clear_map(self):
        self._game_map.clear_map()




    def initialize_fov(self):
        self._fov_recompute = True

        for x, y in fov_map:
            self._fov_map.transparent[x, y] = not game_map.map_array[x][y].block_sight
            self._fov_map.walkable[x, y] = not game_map.map_array[x][y].blocked

        self._map_console.clear()

    def clear_display(self):
        for x in range(self._width):
            for y in range(self._height):
                self._main_console.draw_char(x, y, ' ')




    def rendering(self):
        for elem in self._entities:
            elem.draw(self._main_console)
        self._player.draw(self._main_console)
    



    def update(self):
        self._player_action = 'didnt_take_turn'

        while self._player_action == 'didnt_take_turn':
            self._player_action = self.handling_keys()

        if self._player_action == 'exit':
            return True

        self.clear_display()
        self.rendering()