def player_death(player):
    player.ch = 0x1E
    player.color = (200, 0, 0)

    return 'dead'

def monster_death(monster):
    monster.ch = '%'
    monster.color = (150, 0, 0)
    monster.blocks = False
    monster.ai = None
    monster.name = 'Remains of ' + monster.name + '.'