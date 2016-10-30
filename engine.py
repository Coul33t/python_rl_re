from player import *

import tdl

MOVEMENT_KEYS = {'KP5': [0, 0], 'KP2': [0, 1], 'KP1': [-1, 1], 'KP4': [-1, 0], 'KP7': [-1, -1], 'KP8': [0, -1], 'KP9': [1, -1], 'KP6': [1, 0], 'KP3': [1, 1]}

class Engine:
    def __init__(self, width, height):
        tdl.set_font('fonts/Kelora_16x16_diagonal.png')
        self._main_console = tdl.init(width, height)

        self._width = width
        self._height = height

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





    def clear(self):
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

        self.clear()
        self.rendering()