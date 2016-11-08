class GenericObject:
    def __init__(self, x, y, ch='X', name='NO_NAME', color=(255,255,255), bkg_color=None, blocks=True, always_visible=False):
        self._x = x
        self._y = y
        self._ch = ch
        self._name = name
        self._color = color
        self._bkg_color = bkg_color
        self._blocks = blocks
        self._always_visible = always_visible

    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x

    x = property(_get_x, _set_x)

    def _get_y(self):
        return self._y

    def _set_y(self, y):
        self._y = y

    y = property(_get_y, _set_y)

    def _get_ch(self):
        return self._ch

    def _set_ch(self, ch):
        self._ch = ch

    ch = property(_get_ch, _set_ch)

    def _get_color(self):
        return self._color

    def _set_color(self, color):
        self._color = color

    color = property(_get_color, _set_color)

    def _get_bkg_color(self):
        return self._bkg_color

    def _set_bkg_color(self, bkg_color):
        self._bkg_color = bkg_color

    bkg_color = property(_get_bkg_color, _set_bkg_color)

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = name

    name = property(_get_name, _set_name)

    def _get_blocks(self):
        return self._blocks

    def _set_blocks(self, blocks):
        self._blocks = blocks

    blocks = property(_get_blocks, _set_blocks)

    def _get_always_visible(self):
        return self._always_visible

    def _set_always_visible(self, always_visible):
        self._always_visible = always_visible

    always_visible = property(_get_always_visible, _set_always_visible)




    

    def draw(self, visible_tiles, console):
        if (self._x, self._y) in visible_tiles or self._always_visible:
            console.draw_char(self._x, self._y, self._ch, fg=self._color, bg=self._bkg_color)