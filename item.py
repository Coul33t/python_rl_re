from generic_object import *

class Item(GenericObject):
    def __init__(self, x, y, ch='o', name='item'):
        super(Item, self).__init__(x, y, ch, name, color=(100,100,255))
