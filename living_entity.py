from generic_object import *

class LivingEntity(GenericObject):
    def __init__(self, x, y, ch='@'):
        super(LivingEntity, self).__init__(x, y, ch)

    def move(self, dx, dy):
        self._x += dx
        self._y += dy