from game_map import *
from living_entity import *
from lifeless_entity import *
from player import *
from monster import *
from item import *

from death_functions import *
from ais import *

import tdl
import random as rn

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

MOVEMENT_KEYS = {'KP5': [0, 0], 'KP2': [0, 1], 'KP1': [-1, 1], 'KP4': [-1, 0], 'KP7': [-1, -1], 'KP8': [0, -1], 'KP9': [1, -1], 'KP6': [1, 0], 'KP3': [1, 1]}


class Engine:
    def __init__(self):
        tdl.set_font('fonts/Bedstead_12x20.png')
        self._main_console = tdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT)
        self._map_console = tdl.Console(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT)
        self._panel_console = tdl.Console(PANEL_WIDTH, PANEL_HEIGHT)
        self._message_console = tdl.Console(MESSAGE_WIDTH, MESSAGE_HEIGHT)

        self._game_map = GameMap(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT)
        self._fov_map = tdl.map.Map(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT)
        self._fov_recompute = True

        self._a_star = tdl.map.AStar(DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, self.move_cost, diagnalCost=1)

        self._current_map_level = 1

        self._entities = []
        self._objects = []
        self._visible_tiles = []
        
        self._game_state = 'main_menu'

        self._player = LivingEntity(-1, -1, '@', name='player', player=Player(), death_function=player_death)
        self._player_action = 'didnt_take_turn'

        

    def initialization(self):
        (self._player.x, self._player.y) = self._game_map.create_map()

        for room in self._game_map.rooms:
            self.place_monsters(room)
            self.place_items(room)

        self.initialize_fov()
        self._game_state = 'playing'



        
    def initialize_fov(self):
        self._fov_recompute = True

        for x, y in self._fov_map:
            self._fov_map.transparent[x, y] = not self._game_map.map_array[x][y].block_sight
            self._fov_map.walkable[x, y] = not self._game_map.map_array[x][y].blocked

        self._map_console.clear()





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
                    
                    (dx, dy) = (MOVEMENT_KEYS[user_input.key][0],MOVEMENT_KEYS[user_input.key][1])
                    
                    target = None

                    for entity in self._entities:
                        if entity.x == self._player.x + dx and entity.y == self._player.y + dy and entity and not entity.dead:
                            target = entity

                    if target is not None:
                        self._player.attack(target)


                    elif not self._game_map.is_blocked(self._player.x + dx, self._player.y + dy):
                        self._player.move(dx, dy)

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
            for entity in self._entities:
                if entity.blocks and entity.x == x and entity.y == y:
                    return 10

        return 1



    #TODO: merge place_monster and place_items
    def place_monsters(self, room):
        nb_monsters = rn.randint(0,3)

        for i in range(nb_monsters):

            x = -1
            y = -1

            blocked = True

            while blocked:
                x = rn.randint(room.x1, room.x2 - 1)
                y = rn.randint(room.y1, room.y2 - 1)

                blocked = False

                for entity in self._entities:
                    if entity.x == x and entity.y == y:
                        blocked = True

                if self._game_map.map_array[x][y].blocked:
                    blocked = True

            monster = LivingEntity(x, y, 'M', name='generic_monster', color=(255,50,50), monster=Monster(ai = basic_monster_ai), death_function = monster_death)

            self._entities.append(monster)


    def place_items(self, room):
        nb_items = rn.randint(0,1)

        for i in range(nb_items):
            x = -1
            y = -1

            blocked = True

            while blocked:
                x = rn.randint(room.x1, room.x2 - 1)
                y = rn.randint(room.y1, room.y2 - 1)

                blocked = False

                for entity in self._entities:
                    if entity.x == x and entity.y == y:
                        blocked = True


                if self._game_map.map_array[x][y].blocked:
                    blocked = True

                    

            item = LifelessEntity(x, y, name='generic_item', blocks=False, color=(150,150,255), item=Item())

            self._objects.append(item)


    def send_to_back(self, entity):
        self._entities.remove(entity)
        self._entities.insert(0, entity)



    def clean_console(self, console):
        for x in range(console.width):
            for y in range(console.height):
                console.draw_char(x, y, ' ')

    def set_console(self, console, color):
        for x in range(console.width):
            for y in range(console.height):
                console.draw_char(x, y, ' ', bg=color)





    def clear_display(self):
        for x in range(self._main_console.width):
            for y in range(self._main_console.height):
                self._main_console.draw_char(x, y, ' ')



    
    def rendering(self):
        self.clear_display()
        self._visible_tiles = self._game_map.draw_map(self._fov_map, self._player.x, self._player.y, DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, self._map_console)

        self._main_console.blit(self._map_console, 0, 0, DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, 0, 0)

        for elem in self._objects:
            elem.draw(self._visible_tiles, self._map_console)

        for elem in self._entities:
            elem.draw(self._visible_tiles, self._map_console)
            
        self._player.draw(self._visible_tiles, self._map_console)


        for x in range(0, PANEL_WIDTH):
            for y in range(0, PANEL_HEIGHT):
                if x == 0:
                    self._panel_console.draw_char(x, y, 0xBA, fg=white)

        for x in range(0, MESSAGE_WIDTH):
            for y in range(0, MESSAGE_HEIGHT):
                if y == 0:
                    if x == DUNGEON_DISPLAY_WIDTH:
                        self._message_console.draw_char(x, y, 0xCA, fg=white)
                    else:
                        self._message_console.draw_char(x, y, 0xCD, fg=white)

                else:
                    self._message_console.draw_char(x, y, ' ')

        self._main_console.blit(self._map_console, 0, 0, DUNGEON_DISPLAY_WIDTH, DUNGEON_DISPLAY_HEIGHT, 0, 0)

        self._main_console.blit(self._panel_console, DUNGEON_DISPLAY_WIDTH, 0, CONSOLE_WIDTH, CONSOLE_HEIGHT)

        self._main_console.blit(self._message_console, 0, DUNGEON_DISPLAY_HEIGHT, MESSAGE_WIDTH, MESSAGE_HEIGHT)


    



    def update(self):
        self._player_action = 'didnt_take_turn'

        while self._player_action == 'didnt_take_turn':
            self._player_action = self.handling_keys()

        if self._player_action == 'exit':
            return True

        elif self._game_state == 'playing' and self._player_action is not 'didnt_take_turn':
            for entity in self._entities:
                if entity.monster and entity.monster.ai:
                    entity.monster.take_turn(self._visible_tiles, self._a_star, self._player)

        for elem in self._entities:
            if elem.dead:
                self.send_to_back(elem)

        #self.clear_display()
        self.rendering()