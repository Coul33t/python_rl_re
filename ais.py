def basic_monster_ai(monster, visible_tiles, a_star, player):
    
    if (monster.owner.x, monster.owner.y) in visible_tiles:
        if monster.owner.distance_to(player) > 1:
            new_path = a_star.get_path(monster.owner.x, monster.owner.y, player.x, player.y)
            monster.last_seen_player = ( player.x, player.y)

            if new_path:
                monster.owner.move_towards(new_path[0][0], new_path[0][1])

        else:
            monster.owner.attack(player)


    elif not monster.last_seen_player == (None, None):
        new_path = a_star.get_path(monster.owner.x, monster.owner.y, monster.last_seen_player[0], monster.last_seen_player[1])

        if new_path:
            monster.owner.move_towards(new_path[0][0], new_path[0][1])