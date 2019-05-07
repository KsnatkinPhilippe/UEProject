#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 17:15:15 2019

@author: 3522974
"""

from .tools import *

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


class Attaquant(Strategy):
    def __init__(self , force=4 , surface=50, zone=20, dribble=.4):
        Strategy.__init__(self, "Random")
        self . force = force
        self . surface = surface
        self . zone = zone
        self . dribble = dribble


    def compute_strategy(self, state, id_team, id_player):

        # id_team is 1 or 2
        # id_player starts at 0    
        
        s = SuperState ( state , id_team , id_player , self.dribble)

        if (3-2*s.id_team)*(s.ball.x - GAME_WIDTH*(s.id_team/2)) > 0 :
            if s.gotBall : # condition si le joueur peut touche la balle
                if s.ball.distance( s.goal ) < self.surface : # si la balle est dans la zone de shoot
                    return s.to_goal(self.force)
                else :
                    return s.avancer_en_esquivant( self.zone )
            else :
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


        if s.estLePlusPrès or (3-2*s.id_team)*(s.ball.x - GAME_WIDTH*(s.id_team/3)) < 0:
            return s.to_ball
        
        x=s.goal_ally.x + ((3-2*s.id_team)*GAME_WIDTH/7) # Pos au repos entre les cages et la balle 
#        x=posAtt.x-30 # Pos au repos entre l'attaquant et la balle à 30 d'abscisse
#        return s.move( Vector2D(s.goal_ally.x + ((3-2*s.id_team)*GAME_WIDTH/20), (s.ball.y+s.goal_ally.y)/2) )
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

        
    
class Goal(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player): 
        
        s = SuperState ( state , id_team , id_player )
    
#      return s.move(Vector2D(s.goal_ally.x+10,((s.ball.y + s.goal_ally.y)/2)))
        if s.gotBall :
            return s.passe
        if s.goal_ally.distance(s.ball) < 20 :
            return s.to_ball
#        return s.move(Vector2D(s.goal_ally.x+5,s.ball.y ))
#        return s.move((s.goal_ally-s.player).normalize())
#        return SoccerAction(s.go, s.goal_ally-s.player) 
        return SoccerAction(s.goal_ally-s.player) 
    
class Test(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player): 
        
        s = SuperState ( state , id_team , id_player )
        
        print ("vitesse  =  " , state.ball.vitesse.norm)
        
        if s.gotBall:
            return s.to_goal(6)
        else:
            return s.to_ball
            