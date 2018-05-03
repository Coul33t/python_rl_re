from colors import *

class Tile:
    def __init__(self, ch, blocked=True, block_sight=True, color=white, bkg_color = None):
        self.ch = ch
        self.explored = False
        self.blocked = blocked
        self.block_sight = block_sight
        self.color = color
        self.bkg_color = bkg_color