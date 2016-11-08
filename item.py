from living_entity import *

class Item(LivingEntity):
    def __init__(self, x, y, ch='o', name='item'):
        super(Item, self).__init__(x, y, ch, name, color=(100,100,255))
