#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 18:54:13 2019

@author:  3522974
"""


from tools import *

class Defense (Strategy):
    def __init__(self , force=2 , surface=25, zone=30, dribble=1.34):
        Strategy.__init__(self, "Random")
        self . force = force
        self . surface = surface
        self . zone = zone
        self . dribble = dribble


    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState ( state , id_team , id_player , self.dribble)
        
        if s.gotBall:
            return s.shootOpti
        else :
            if (s.id_team == 1):
                if (s.ball.x > GAME_WIDTH/2):
                    return s.position_volley
                else :
                    return s.to_ball
            else :
                if (s.ball.x < GAME_WIDTH/2):
                    return s.position_volley
                else :
                    return s.to_ball     
        
        