from generic_object import *

#TODO: add a generic class for all items/props/object (find a good name ...)
# then add an item property (composition)
class Item(GenericObject):
    def __init__(self, x, y, ch='o', name='item'):
        super(Item, self).__init__(x, y, ch, name, color=(100,100,255))
