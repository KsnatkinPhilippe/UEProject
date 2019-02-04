# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, PLAYER_RADIUS


class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        ball = state.ball.position
        player = state.player_state(id_team, id_player).position
        goal = Vector2D(GAME_WIDTH * (2 - id_team), GAME_HEIGHT/2)
        if player.distance(ball) < PLAYER_RADIUS + BALL_RADIUS:
            return SoccerAction(shoot=goal-player)
        else :
            return SoccerAction(acceleration=ball-player)


# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Fonceur", FonceurStrategy())  # Random strategy
team2.add("Static", Strategy())   # Static strategy

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)


