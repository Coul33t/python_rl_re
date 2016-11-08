from generic_object import *

class LivingEntity(GenericObject):
    def __init__(self, x, y, ch='@', name='NO_NAME', color=(255,255,255), bkg_color=None, blocks=True, always_visible=False):
        super(LivingEntity, self).__init__(x, y, ch, name, color, bkg_color, blocks, always_visible)

    def move(self, dx, dy):
        self._x += dx
        self._y += dy