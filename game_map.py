from tile import *
from colors import *
from geometry import *

import math

import random as rn

import pdb

MAP_TILES = {'wall': '#', 'floor': '.'}
NOT_VISIBLE_COLORS = {MAP_TILES['floor']: (25, 25, 25), MAP_TILES['wall']: (50, 50, 50)}
VISIBLE_COLORS = {MAP_TILES['floor']: (100, 100, 100), MAP_TILES['wall']: (150, 150, 150)}

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 20

MIN_ROOM = 5
MAX_ROOM = 30
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 10

class GameMap:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._map_array = [[Tile(MAP_TILES['wall'], color=light_gray) for y in range(height)] for x in range(width)]


    def _get_width(self):
        return self._width

    def _set_width(self, width):
        self._width = width

    width = property(_get_width, _set_width)

    def _get_height(self):
        return self._height

    def _set_height(self, height):
        self._height = height

    height = property(_get_height, _set_height)

    def _get_map_array(self):
        return self._map_array

    def _set_map_array(self, map_array):
        self._map_array = map_array

    map_array = property(_get_map_array, _set_map_array)




    def is_visible_tile(self, x, y):
        x = int(x)
        y = int(y)

        if x >= MAP_WIDTH or x < 0:
            return False

        elif y >= MAP_HEIGHT or y < 0:
            return False

        elif self._map_array[x][y].blocked:
            return False

        elif self._map_array[x][y].block_sight:
            return False

        else:
            return True




    def is_blocked(self, x, y):
        if self.map_array[x][y].blocked:
            return True

        return False



    def clear_map(self):
        self._map_array = [[Tile(MAP_TILES['wall'], color=light_gray) for y in range(self._height)] for x in range(self._width)]


    def create_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self._map_array[x][y].ch = MAP_TILES['floor']
                self._map_array[x][y].blocked = False
                self._map_array[x][y].block_sight = False

    def carve_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self._map_array[x][y].ch = MAP_TILES['floor']
            self._map_array[x][y].blocked = False
            self._map_array[x][y].block_sight = False

    def carve_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self._map_array[x][y].ch = MAP_TILES['floor']
            self._map_array[x][y].blocked = False
            self._map_array[x][y].block_sight = False





    def create_map(self):

        rooms = []
        num_rooms = 0

        monster_count = 0

        self.clear_map()

        while num_rooms < MAX_ROOM:

            if num_rooms >= MIN_ROOM:
                if rn.random() <= (num_rooms - MIN_ROOM)/(MAX_ROOM - MIN_ROOM):
                    break

            carved = False

            while not carved:

                carved = True

                w = rn.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
                h = rn.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
                x = rn.randint(1, self._width - w - 1)
                y = rn.randint(1, self._height - h - 1)

                new_room = Rect(x, y, w, h)

                if rooms:
                    for other_room in rooms:
                        if new_room.intersect(other_room):
                            carved = False
                else:
                    carved = True

            self.create_room(new_room)

            (new_x, new_y) = new_room.get_center()

            if num_rooms == 0:
                return_coordinates = (new_x, new_y)

            else:
                closest_room = [-1, -1]
                for i, other_room in enumerate(rooms):
                    if closest_room == [-1, -1]:
                        closest_room = list(other_room.get_center())
                    else:
                        if math.sqrt(pow(other_room.x1 - x, 2) + pow(other_room.y1 - y, 2)) < math.sqrt(pow(closest_room[0] - x, 2) + pow(closest_room[1] - y, 2)):
                            closest_room = list(other_room.get_center())

                if rn.random() > 0.5:
                    self.carve_h_tunnel(x, closest_room[0], y)
                    self.carve_v_tunnel(y, closest_room[1], closest_room[0])
                else:
                    self.carve_v_tunnel(y, closest_room[1], x)
                    self.carve_h_tunnel(x, closest_room[0], closest_room[1])


            rooms.append(new_room)
            print('room added')
            num_rooms += 1

        return return_coordinates




    def draw_map(self, fov_map, player_x, player_y, display_x, display_y, map_console):

        visible_tiles = []

        visible_tiles_iter = fov_map.compute_fov(player_x, player_y, radius=TORCH_RADIUS, light_walls=FOV_LIGHT_WALLS)


        for tile in visible_tiles_iter:
            visible_tiles.append(tile)


        for x in range(display_x):
            for y in range(display_y):

                if (x, y) in visible_tiles:
                    self._map_array[x][y].explored = True
                    map_console.draw_char(x, y, self._map_array[x][y].ch, fg=VISIBLE_COLORS[self._map_array[x][y].ch], bg=self._map_array[x][y].bkg_color)
                else:
                    if self._map_array[x][y].explored:
                        map_console.draw_char(x, y, self._map_array[x][y].ch, fg=NOT_VISIBLE_COLORS[self._map_array[x][y].ch], bg=self._map_array[x][y].bkg_color)