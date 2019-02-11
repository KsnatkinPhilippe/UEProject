#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:59:17 2019

@author: 3700067
"""

#
from Module.tools import*

class Attaquant(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")


    def compute_strategy(self, state, id_team, id_player):

        # id_team is 1 or 2
        # id_player starts at 0    
        
        s = SuperState ( state , id_team , id_player )
        
#        print ((state.ball.vitesse + s.ball).norm_max( maxBallAcceleration ) - s.player )
        
        
        if s.player.distance( s.ball ) <= PLAYER_RADIUS + BALL_RADIUS : # condition si le joueur peut touche la balle
            if s.ball.distance( s.goal ) < 20 : # si la balle est dans la zone de shoot
                return s.tirer_au_but
            else :
                return s.avancer_en_esquivant( 40 )
        else :
            return s.foncerVersBallonV2


class Bourrin(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")


    def compute_strategy(self, state, id_team, id_player):

        # id_team is 1 or 2
        # id_player starts at 0

       #Foncer vers la balle, vers les buts et tirer au but

        
        #Si il a la balle tir au but sinon continu sa course éfrénée
        if (state.player_state( id_team , id_player ).position.distance( state.ball.position ) < PLAYER_RADIUS + BALL_RADIUS):
            if (GAME_WIDTH - state.ball.position.x <  40):
                return SoccerAction(shoot = (Vector2D(GAME_WIDTH * ( 2 - id_team ), GAME_HEIGHT /2.)- state.ball.position).norm_max(maxPlayerShoot) )
            else:
                return SoccerAction(shoot = (Vector2D(GAME_WIDTH * ( 2 - id_team ), GAME_HEIGHT /2.) - state.ball.position).norm_max(maxPlayerShoot))

        else :
            return SoccerAction(acceleration = (state.ball.position - state.player_state(id_team, id_player).position).norm_max( maxPlayerAcceleration )) 



class Defenseur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")


    def compute_strategy(self, state, id_team, id_player):

        # id_team is 1 or 2
        # id_player starts at 0    
        
        s = SuperState ( state , id_team , id_player )
        
        if (( 2 - id_player ) * GAME_WIDTH / 2  <= s.ball.x <= ( 3 - id_player ) * GAME_WIDTH / 2) or ( s.team_gotBall ) :
            return s.se_replacer
        else :
            return s.foncerVersBallonV2
            

# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Principal", Defenseur())  # Random strategy
team2.add("Static", Strategy())   # Static strategy

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
