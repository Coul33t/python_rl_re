from actor import *
from math import hypot
import pdb
class Monster(Actor):
    def __init__(self, x, y, ch='M', name='monster',
                 detection_radius=10):
        super(Monster, self).__init__(x, y, ch, name, color=(255,100,100))
        self.detection_radius = detection_radius
        self.last_seen_player = (None, None)

    def dst(self, p):
        return hypot(p.x - self.x, p.y - self.y)

    def take_turn(self, player, a_star, entities):
        if self.dst(player) <= self.detection_radius:
            # Round because of the diagonals (round(1.41) = 1)
            if round(self.dst(player)) > 1:
                new_path = a_star.get_path(self.x, self.y, player.x, player.y)
                self.last_seen_player = (player.x, player.y)

                if new_path:
                    if (new_path[0][0], new_path[0][1]) not in [(en.x, en.y) for en in entities if en.blocks]:
                        self.move(new_path[0][0] - self.x, new_path[0][1] - self.y)
            else:
                self.attack(player)

