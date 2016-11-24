from generic_object import *
import math

DEBUG = True

class LivingEntity(GenericObject):
    def __init__(self, x, y, ch='@', name='NO_NAME', hp=10, stamina=10, mana=10, 
        defense=0, melee_dmg=1, ranged_dmg=0, level=1, xp=0, xp_given=0, dead=False,
        color=(255,255,255), bkg_color=None, blocks=True, always_visible=False,
        player=None, monster=None, death_function=None):
        
        super(LivingEntity, self).__init__(x, y, ch, name, color, bkg_color, blocks, always_visible)
        
        self._hp = hp
        self._max_hp = hp
        self._stamina = stamina
        self._max_stamina = stamina
        self._mana = mana
        self._max_mana = mana
        self._defense = defense
        self._melee_dmg = melee_dmg
        self._ranged_dmg = ranged_dmg
        self._level = level
        self._xp = xp
        self._xp_given = xp_given
        self._dead = dead

        self._player = player
        if self._player:
            self._player.owner = self

        self._monster = monster
        if self._monster:
            self._monster.owner = self

        self._death_function = death_function





    def _get_max_hp(self):
        return self._max_hp

    def _set_max_hp(self, max_hp):
        self._max_hp = max_hp

    max_hp = property(_get_max_hp, _set_max_hp)

    def _get_hp(self):
        return self._hp

    def _set_hp(self, hp):
        self._hp = hp

    hp = property(_get_hp, _set_hp)

    def _get_stamina(self):
        return self._stamina

    def _set_stamina(self, stamina):
        self._stamina = stamina

    stamina = property(_get_stamina, _set_stamina)

    def _get_max_stamina(self):
        return self._max_stamina

    def _set_max_stamina(self, max_stamina):
        self._max_stamina = max_stamina

    max_stamina = property(_get_max_stamina, _set_max_stamina)

    def _get_defense(self):
        return self._defense

    def _set_defense(self, defense):
        self._defense = defense

    defense = property(_get_defense, _set_defense)

    def _get_melee_dmg(self):
        return self._melee_dmg

    def _set_melee_dmg(self, melee_dmg):
        self._melee_dmg = melee_dmg

    melee_dmg = property(_get_melee_dmg, _set_melee_dmg)

    def _get_ranged_dmg(self):
        return self._ranged_dmg

    def _set_ranged_dmg(self, ranged_dmg):
        self._ranged_dmg = ranged_dmg

    ranged_dmg = property(_get_ranged_dmg, _set_ranged_dmg)

    def _get_level(self):
        return self._level

    def _set_level(self, level):
        self._level = level

    level = property(_get_level, _set_level)

    def _get_xp(self):
        return self._xp

    def _set_xp(self, xp):
        self._xp = xp

    xp = property(_get_xp, _set_xp)

    def add_xp(self, xp):
        self._xp += xp

    def _get_xp_given(self):
        return self._xp_given

    def _set_xp_given(self, xp_given):
        self._xp_given = xp_given

    xp_given = property(_get_xp_given, _set_xp_given)

    def _get_dead(self):
        return self._dead

    def _set_dead(self, dead):
        self._dead = dead

    dead = property(_get_dead, _set_dead)

    def _get_player(self):
        return self._player

    def _set_player(self, player):
        pass

    player = property(_get_player, _set_player)

    def _get_monster(self):
        return self._monster

    def _set_monster(self, monster):
        self._monster = monster

    monster = property(_get_monster, _set_monster)





    def move(self, dx, dy):
        self._x += dx
        self._y += dy


    def move_towards(self, target_x, target_y):

        dx = target_x - self._x
        dy = target_y - self._y

        self.move(dx, dy)

    def distance_to(self, other):
        return round(math.sqrt((other.x - self._x)**2 + (other.y - self._y)**2))

    def attack(self, target):
        dmg = self._melee_dmg - target._defense

        if DEBUG:
            print('{} ({},{}) attacks {} ({},{})'.format(self._name, self._x, self._y, target.name, target.x, target.y))
            print('{} does {} damage to {} ({}/{})'.format(self._name, dmg, target.name, target.hp, target.max_hp))

        target.take_damage(dmg)

        


    def take_damage(self, dmg):
        self._hp -= dmg
        
        if self._hp <= 0:
            self._hp = 0

            self._dead = True

            if self._death_function:
                self._death_function(self)


    def heal(self, heal):
        self._hp += heal

        if self._hp > self._max_hp:
            self._hp = self._max_hp

