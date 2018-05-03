from actor import *

class Player(Actor):
    def __init__(self, x, y, ch='@'):
        super(Player, self).__init__(x, y, ch, name='player')
