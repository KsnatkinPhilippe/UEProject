#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 17:15:15 2019

@author: 3522974
"""

from .tools import *

class Attaquant(Strategy):
    def __init__(self , force=4 , surface=50, zone=20, dribble=2.):
        Strategy.__init__(self, "Random")
        self . force = force
        self . surface = surface
        self . zone = zone
        self . dribble = dribble


    def compute_strategy(self, state, id_team, id_player):
  
        
        s = SuperState ( state , id_team , id_player , self.dribble)

        if s.gotBall : # condition si le joueur peut touche la balle
            return s.passe

        if s.estLePlusPrès:
            return s.to_ball
                
        return s.move(Vector2D((3-2*s.id_team)*GAME_WIDTH * 6/8+s.goal_ally.x , GAME_HEIGHT * 3/8. ))

class Defenseur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")


    def compute_strategy(self, state, id_team, id_player): 
        
        s = SuperState ( state , id_team , id_player )

        if s.gotBall :
            return s.passe


        if s.estLePlusPrès or (3-2*s.id_team)*(s.ball.x - GAME_WIDTH*(s.id_team/4)) < 0:
            return s.to_ball
        
        x=s.goal_ally.x + ((3-2*s.id_team)*GAME_WIDTH/10) # Pos au repos entre les cages et la balle 
        return s.move( s.placerEntrePourxDef(x , s.ball , s.goal_ally) )

        
class MilieuDef(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")


    def compute_strategy(self, state, id_team, id_player): 
        
        s = SuperState ( state , id_team , id_player )

        if s.gotBall :
            return s.passe

        if s.estLePlusPrès:
            return s.to_ball        

        if (s.ball.x >= GAME_WIDTH*1/4  and s.ball.x <= GAME_WIDTH * 3/4 and s.ball.y <= GAME_HEIGHT * 1/2) :
            distAtt , ( id_teamAtt , id_playerAtt ) = s.AdvAtt
            posAtt = state.player_state( id_teamAtt , id_playerAtt  ).position
            x=(s.ball.x+posAtt.x)/2 # Pos au repos entre l'attaquant et la balle
            return s.move( s.placerEntrePourxDef(x , s.ball , posAtt) )
        
        return s.move(Vector2D((3-2*s.id_team)*(GAME_WIDTH*3/8)  + s.goal_ally.x,GAME_HEIGHT*9/32)) 
    

class MilieuAtt(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")


    def compute_strategy(self, state, id_team, id_player): 
        
        s = SuperState ( state , id_team , id_player )

        if s.gotBall :
            
            return s.passe

        if s.estLePlusPrès or(s.ball.x >= GAME_WIDTH*1/4  and s.ball.x <= GAME_WIDTH * 3/4 and s.ball.y >= GAME_HEIGHT * 1/2):
            return s.to_ball
        
        return s.move(Vector2D((3-2*s.id_team)*(GAME_WIDTH*5/8)  + s.goal_ally.x,GAME_HEIGHT*23/32))
