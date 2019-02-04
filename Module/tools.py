class SuperState(object):
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
    @property
    def ball(self):
        return self.state.ball.position
        
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position
        
    @property
    def opponent(self):
        #return self.state.player_state(3 - self.id_team, 0).position
        opponents = []
        for idteam, idplayer in self.state.players:
            if idteam != self.id_team:
                opponents.append((idplayer, self.player.distance(self.state.player_state(idteam, idplayer).position)))
        AdvPlusProche = opponents[0]
        for idplayer, distance in opponents:
            if distance < AdvPlusProche[1]:
                AdvPlusProche = idplayer, distance
        return AdvPlusProche[1]
            
        
        
