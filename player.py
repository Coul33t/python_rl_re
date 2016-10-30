from generic_object import *

class Player(GenericObject):
    def __init__(self, x, y, ch='@'):
        super(Player, self).__init__(x, y, ch)
