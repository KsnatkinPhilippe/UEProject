# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, PLAYER_RADIUS
from tools import SuperState


class AttackStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "ATK")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        s = SuperState(state, id_team, id_player)
        ball = s.ball
        player = s.player
        goal = Vector2D(GAME_WIDTH * (2 - id_team), GAME_HEIGHT/2)
        
        if player.distance(ball) < PLAYER_RADIUS + BALL_RADIUS:
            return SoccerAction(shoot=(goal-player))
        else :
            """s.opponent[1]
            """
            
            
            
            
            if player.distance(goal)<50:
                return SoccerAction(shoot=(goal-player) / 10)
            else :
                if s.opponent < 40:
                    if s.id_team == 1:
                        return SoccerAction(shoot=Vector2D(1,1))
                    else :
                        return SoccerAction(shoot=Vector2D(-1,-1))
                else :
                    return SoccerAction(shoot=(goal-player) / 50)
        else :
            return SoccerAction(acceleration=ball-player)


# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("ATK", AttackStrategy())  # Random strategy
team2.add("ADV", AttackStrategy())   # Static strategy

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
