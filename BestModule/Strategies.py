#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 17:15:15 2019

@author: 3522974
"""

from .tools import *

class Attaquant(Strategy):
    def __init__(self , force=1.2 , surface=15, zone=20, dribble=1.5):
        Strategy.__init__(self, "Random")
        self . force = force
        self . surface = surface
        self . zone = zone
        self . dribble = dribble


    def compute_strategy(self, state, id_team, id_player):

        # id_team is 1 or 2
        # id_player starts at 0    
        
        s = SuperState ( state , id_team , id_player , self.dribble)

        
        if s.gotBall : # condition si le joueur peut touche la balle
            if s.ball.distance( s.goal ) < self.surface : # si la balle est dans la zone de shoot
                return s.to_goal(self.force)
#                return s.tirer_au_but
            else :
                return s.avancer_en_esquivant( self.zone )
        else :
            return s.to_ball


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
        
        s = SuperState ( state , id_team , id_player )

        if s.gotBall :
            return s.tirer_au_but
        if 2*(1.5-id_team)*(GAME_WIDTH/4 - s.ball.x) <= 0 :
            return s.positionnement
        else :
            return s.to_ball
            