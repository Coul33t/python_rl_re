from generic_object import *

class LifelessEntity(GenericObject):
    def __init__(self, x, y, ch='o', name='NO_NAME', item=None):
        super(LifelessEntity, self).__init__(x, y, ch, name, color=(100,100,255))

        self._item = item
        if self._item:
            self._item.owner = self