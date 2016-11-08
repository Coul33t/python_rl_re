from living_entity import *

class Player(LivingEntity):
    def __init__(self, x, y, ch='@'):
        super(Player, self).__init__(x, y, ch, name='player')
