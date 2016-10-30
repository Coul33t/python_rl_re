class Rect:
    def __init__(self, x, y, w, h):
        self._x1 = x
        self._y1 = y
        self._x2 = x + w
        self._y2 = y + h

    def _get_x1(self):
        return self._x1

    def _set_x1(self, x1):
        self._x1 = x1

    x1 = property(_get_x1, _set_x1)

    def _get_y1(self):
        return self._y1

    def _set_y1(self, y1):
        self._y1 = y1

    y1 = property(_get_y1, _set_y1)

    def _get_x2(self):
        return self._x2

    def _set_x2(self, x2):
        self._x2 = x2

    x2 = property(_get_x2, _set_x2)

    def _get_y2(self):
        return self._y2

    def _set_y2(self, y2):
        self._y2 = y2

    y2 = property(_get_y2, _set_y2)

    def get_center(self):
        return ((int)((self._x1 + self._x2)/2), (int)((self._y1 + self._y2)/2))

    def intersect(self, other_rect):
        return (self._x1 <= other_rect.x2 and self._x2 >= other_rect.x1 and
                self._y1 <= other_rect.y2 and self._y2 >= other_rect.y1)