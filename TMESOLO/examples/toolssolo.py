#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 17:06:22 2019

@author:  3522974
"""

from soccersimulator import *

class StateSolo ( object ):
    def __init__ ( self , state , id_team , id_player , dribble=12 , force=12):
            self.state = state
            self.id_team = id_team
            self.id_player = id_player
            self . dribble = dribble
            self . force = force
            
    @property 
    def position_volley( self ):
        if (self.id_team == 1):
            return self.move(Vector2D(GAME_WIDTH/4,GAME_HEIGHT/2))
        else :
            return self.move(Vector2D((GAME_WIDTH/4)*3,GAME_HEIGHT/2))