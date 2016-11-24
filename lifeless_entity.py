from generic_object import *

class LifelessEntity(GenericObject):
    def __init__(self, x, y, ch='o', name='NO_NAME', color=(255,255,255), bkg_color=None, blocks=True, always_visible=False, item=None):
        super(LifelessEntity, self).__init__(x, y, ch, name, color, bkg_color, blocks, always_visible)

        self._item = item
        if self._item:
            self._item.owner = self