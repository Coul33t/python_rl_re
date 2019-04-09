from player import *
from game_map import *
from monster import *
from item import *

import tdl
import random as rn

import pdb

import time

CONSOLE_WIDTH = 100
CONSOLE_HEIGHT = 40

MESSAGE_WIDTH = CONSOLE_WIDTH
MESSAGE_HEIGHT = 10

DUNGEON_DISPLAY_WIDTH = 80
DUNGEON_DISPLAY_HEIGHT = CONSOLE_HEIGHT-MESSAGE_HEIGHT

PANEL_WIDTH = CONSOLE_WIDTH - DUNGEON_DISPLAY_WIDTH
PANEL_HEIGHT = CONSOLE_HEIGHT - MESSAGE_HEIGHT

MAP_WIDTH = 200
MAP_HEIGHT = 200

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 20

MAP_TILES = {'wall': '#', 'floor': '.'}
NOT_VISIBLE_COLORS = {'.': (25, 25, 25), '#': (50, 50, 50)}
VISIBLE_COLORS = {'.': (100, 100, 100), '#': (150, 150, 150)}

MOVEMENT_KEYS = {'5': [0, 0], '2': [0, 1], '1': [-1, 1], '4': [-1, 0], '7': [-1, -1], '8': [0, -1], '9': [1, -1], '6': [1, 0], '3': [1, 1]}


class Engine:
    def __init__(self):
        tdl.set_font('fonts/Bedstead_12x20.png')
        self.main_console = tdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT)
        self.map_console = tdl.Console(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT)
        self.panel_console = tdl.Console(PANEL_WIDTH, PANEL_HEIGHT)
        self.message_console = tdl.Console(MESSAGE_WIDTH, MESSAGE_HEIGHT)

        self.game_map = GameMap(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT)
        self.fov_map = tdl.map.Map(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT)
        self.fov_recompute = True

        self.a_star = tdl.map.AStar(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, self.move_cost, diagnalCost=1)

        self.current_map_level = 1

        self.entities = []

        self.game_state = 'main_menu'

        self.player = Player(-1, -1, '@')
        self.player_action = 'didnt_take_turn'



    def initialization(self):
        (self.player.x, self.player.y) = self.game_map.create_map()

        for room in self.game_map.rooms:
            self.place_monsters(room)
            self.place_items(room)

        self.initialize_fov()
        self.game_state = 'playing'




    def initialize_fov(self):
        self.fov_recompute = True

        for x, y in self.fov_map:
            self.fov_map.transparent[x, y] = not self.game_map.map_array[x][y].block_sight
            self.fov_map.walkable[x, y] = not self.game_map.map_array[x][y].blocked

        self.map_console.clear()





    def handling_keys(self):
        user_input = None

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event

        if user_input:
            if user_input.key == 'ESCAPE':
                return 'exit'

            if self.game_state == 'playing':
                # Movement and/or attack
                if user_input.text in MOVEMENT_KEYS:

                    (dx, dy) = (MOVEMENT_KEYS[user_input.text][0],MOVEMENT_KEYS[user_input.text][1])

                    # Ok
                    if not self.is_blocked(self.player.x + dx, self.player.y + dy):
                        self.player.move(dx, dy)
                        self.fov_recompute = True
                        return 'moved'
                    # There's a monster, attack
                    elif not self.game_map.is_blocked(self.player.x, self.player.y):
                        act = self.monster_here(self.player.x + dx, self.player.y + dy)
                        if act:
                            self.player.attack(act)


                else:
                    return 'didnt_take_turn'

        else:
            return 'didnt_take_turn'



    def monster_here(self, x, y):
        for en in self.entities:
            if isinstance(en, Actor) and en.x == x and en.y == y:
                return en
        return False

    def is_blocked(self, x, y):
        if self.game_map.is_blocked(x, y):
            return True

        if (x, y) in [(en.x, en.y) for en in self.entities if en.blocks]:
            return True




    def move_cost(self, x, y):
        if self.game_map.is_blocked(x, y):
            return 0

        else:
            for en in self.entities:
                if en.blocks and en.x == x and en.y == y:
                    # 10 means that if there's an entity in the path, the current actor
                    # will try to get around it in a max radius of 10 tiles
                    return 10

        return 1




    def place_monsters(self, room):
        nb_monsters = rn.randint(0,3)

        for i in range(nb_monsters):
            x = rn.randint(room.x1, room.x2 - 1)
            y = rn.randint(room.y1, room.y2 - 1)

            monster = Monster(x, y)

            self.entities.append(monster)


    def place_items(self, room):
        nb_items = rn.randint(0,1)

        for i in range(nb_items):
            x = -1
            y = -1

            while self.game_map.map_array[x][y].blocked:
                x = rn.randint(room.x1, room.x2 - 1)
                y = rn.randint(room.y1, room.y2 - 1)

            item = Item(x, y)

            self.entities.append(item)



    def clean_console(self, console):
        for x in range(console.width):
            for y in range(console.height):
                console.draw_char(x, y, ' ')

    def set_console(self, console, color):
        for x in range(console.width):
            for y in range(console.height):
                console.draw_char(x, y, ' ', bg=color)





    def clear_display(self):
        for x in range(self.main_console.width):
            for y in range(self.main_console.height):
                self.main_console.draw_char(x, y, ' ')




    def rendering(self):
        self.clear_display()

        visible_tiles = []

        visible_tiles = self.game_map.draw_map(self.fov_map, self.fov_recompute, self.player.x, self.player.y, DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, self.map_console)

        self.main_console.blit(self.map_console, 0, 0, DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, 0, 0)

        for en in self.entities:
            en.draw(visible_tiles, self.map_console)

        self.player.draw(visible_tiles, self.map_console)

        for x in range(0, PANEL_WIDTH):
            for y in range(0, PANEL_HEIGHT):
                if x == 0:
                    self.panel_console.draw_char(x, y, 0xBA, fg=white)

        for x in range(0, MESSAGE_WIDTH):
            for y in range(0, MESSAGE_HEIGHT):
                if y == 0:
                    if x == DUNGEON_DISPLAY_WIDTH:
                        self.message_console.draw_char(x, y, 0xCA, fg=white)
                    else:
                        self.message_console.draw_char(x, y, 0xCD, fg=white)

                else:
                    self.message_console.draw_char(x, y, ' ')

        self.main_console.blit(self.map_console, 0, 0, DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, 0, 0)

        self.main_console.blit(self.panel_console, DUNGEON_DISPLAY_WIDTH, 0, CONSOLE_WIDTH, CONSOLE_HEIGHT)

        self.main_console.blit(self.message_console, 0, DUNGEON_DISPLAY_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT)





    def check_death(self):
        for en in self.entities:
            if isinstance(en, Actor) and en.hp <= 0:
                self.entities.remove(en)

    def update(self):
        self.player_action = 'didnt_take_turn'

        while self.player_action == 'didnt_take_turn':
            self.player_action = self.handling_keys()

        if self.player_action == 'exit':
            return True

        for en in self.entities:
            if isinstance(en, Actor):
                en.take_turn(self.player, self.a_star, self.entities)

        self.check_death()

        tdl.flush()