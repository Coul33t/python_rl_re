class Monster:
    
    def __init__(self, ai=None):
        
        self._ai = ai
        if self._ai:
            self._ai.owner = self

        self._last_seen_player = (None, None)

    def _get_ai(self):
        return self._ai

    def _set_ai(self, ai):
        self._ai = ai

    ai = property(_get_ai, _set_ai)

    def _get_last_seen_player(self):
        return self._last_seen_player

    def _set_last_seen_player(self, last_seen_player):
        self._last_seen_player = last_seen_player

    last_seen_player = property(_get_last_seen_player, _set_last_seen_player)

    def take_turn(self, visible_tiles, a_star, player):
        if self._ai:
            self._ai(self, visible_tiles, a_star, player)


    

