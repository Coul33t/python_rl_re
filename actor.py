from generic_object import *

class Actor(GenericObject):
    def __init__(self, x, y, ch='@', name='NO_NAME', color=(255,255,255), 
                 bkg_color=None, blocks=True, always_visible=False, hp=10,
                 dmg=2):
        super(Actor, self).__init__(x, y, ch, name, color, bkg_color, blocks, always_visible)
        self.hp = hp
        self.dmg = dmg


    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def attack(self, enemy):
        enemy.hp -= self.dmg