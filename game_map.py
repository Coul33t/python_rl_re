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
        self.width = width
        self.height = height
        self.map_array = [[Tile(MAP_TILES['wall'], color=light_gray) for y in range(height)] for x in range(width)]
        self.rooms = []
        self.visible_tiles = []


    def is_visible_tile(self, x, y):
        x = int(x)
        y = int(y)

        if x >= MAP_WIDTH or x < 0:
            return False

        elif y >= MAP_HEIGHT or y < 0:
            return False

        elif self.map_array[x][y].blocked:
            return False

        elif self.map_array[x][y].block_sight:
            return False

        else:
            return True




    def is_blocked(self, x, y):
        if self.map_array[x][y].blocked:
            return True

        return False



    def clear_map(self):
        self.map_array = [[Tile(MAP_TILES['wall'], color=light_gray) for y in range(self.height)] for x in range(self.width)]


    def create_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.map_array[x][y].ch = MAP_TILES['floor']
                self.map_array[x][y].blocked = False
                self.map_array[x][y].block_sight = False

    def carve_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map_array[x][y].ch = MAP_TILES['floor']
            self.map_array[x][y].blocked = False
            self.map_array[x][y].block_sight = False

    def carve_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map_array[x][y].ch = MAP_TILES['floor']
            self.map_array[x][y].blocked = False
            self.map_array[x][y].block_sight = False





    def create_map(self):

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
                x = rn.randint(1, self.width - w - 1)
                y = rn.randint(1, self.height - h - 1)

                new_room = Rect(x, y, w, h)

                if self.rooms:
                    for other_room in self.rooms:
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
                for i, other_room in enumerate(self.rooms):
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


            self.rooms.append(new_room)

            num_rooms += 1

        return return_coordinates




    def draw_map(self, fov_map, recompute, player_x, player_y, display_x, display_y, map_console):

        if recompute or not visible_tiles:
            visible_tiles_iter = fov_map.compute_fov(player_x, player_y, radius=TORCH_RADIUS, light_walls=FOV_LIGHT_WALLS)
            self.visible_tiles = list(visible_tiles_iter)

        for x in range(display_x):
            for y in range(display_y):

                if (x, y) in self.visible_tiles:
                    self.map_array[x][y].explored = True
                    map_console.draw_char(x, y, self.map_array[x][y].ch, fg=VISIBLE_COLORS[self.map_array[x][y].ch], bg=self.map_array[x][y].bkg_color)
                else:
                    if self.map_array[x][y].explored:
                        map_console.draw_char(x, y, self.map_array[x][y].ch, fg=NOT_VISIBLE_COLORS[self.map_array[x][y].ch], bg=self.map_array[x][y].bkg_color)

        return self.visible_tiles