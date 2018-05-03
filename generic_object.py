class GenericObject:
    def __init__(self, x, y, ch='X', name='NO_NAME', color=(255,255,255), bkg_color=None, blocks=True, always_visible=False):
        self.x = x
        self.y = y
        self.ch = ch
        self.name = name
        self.color = color
        self.bkg_color = bkg_color
        self.blocks = blocks
        self.always_visible = always_visible

    def draw(self, visible_tiles, console):
        if (self.x, self.y) in visible_tiles or self.always_visible:
            console.draw_char(self.x, self.y, self.ch, fg=self.color, bg=self.bkg_color)