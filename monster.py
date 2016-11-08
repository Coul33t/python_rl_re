from living_entity import *

class Monster(LivingEntity):
    def __init__(self, x, y, ch='M', name='monster'):
        super(Monster, self).__init__(x, y, ch, name, color=(255,100,100))



    def take_turn(self):
        pass
