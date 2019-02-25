#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:34:13 2019

@author: 3700067
"""

from soccersimulator import *

class SuperState ( object ):
    def __init__ ( self , state , id_team , id_player ):
            self.state = state
            self.id_team = id_team
            self.id_player = id_player

#def __getattr__ ( self , attr ):
#    return getattr ( self . state , attr )

    @property
    def ball ( self ):
        return self.state.ball.position

    @property
    def player ( self ):
        return self.state.player_state ( self.id_team , self.id_player ).position

    @property
    def goal ( self ):
        return Vector2D( GAME_WIDTH * ( 2 - self.id_team  ), GAME_HEIGHT /2. ) 
    
    @property
    def goal_ally( self ):
        return Vector2D( GAME_WIDTH * ( self.id_team - 1 ), GAME_HEIGHT /2. )
    
    @property
    def to_ball( self ) : #aller vers la futur position du ballon
        return self.move(self.state.ball.vitesse.norm_max( maxBallAcceleration ) + self.ball)


    def shoot( self , cible , norme) :
        return SoccerAction( shoot = ( cible - self.ball ).normalize() * norme ) 
    
    def move( self , cible ): # aller vers la cible immobile
        return SoccerAction( acceleration = ( cible - self.player ).normalize() * maxPlayerAcceleration )
        
    @property #vitesse du joueur a opti
    def dribbler( self ) : # foncer vers les buts avec le ballon
        return self.shoot( self.goal , maxPlayerShoot / 4 )

    @property
    def tirer_au_but( self ):
        return self.shoot( self.goal , maxPlayerShoot)

    def to_goal( self , norme):
        return self.shoot( self.goal , norme)

    @property
    def adversaire_le_plus_proche( self ) :    #trouve l'adversaire le plus proche devant soit renvoi un tuple ( distance , id_ player , (distance en y , distance en x) , id_team ) 
        return  min([( self.player.distance( self.state.player_state( id_team , id_player ).position ) ,  id_player , (self.state.player_state( id_team , id_player ).position.y - self.player.y, self.state.player_state( id_team , id_player ).position.x - self.player.x ) , id_team ) for ( id_team , id_player ) in self.state.players if id_team != self.id_team])



    def avancer_en_esquivant( self , zone ) :     #prend en argument la zone de souveraineté du joueur et renvoie la marche a suivre
        
        dist_opp, id_opp, (diff_y, diff_x), id_team_opp = self.adversaire_le_plus_proche        
        adversaire = self.state.player_state( id_team_opp , id_opp).position        
        dir_adv = adversaire - self.ball 

        if ((2*(1.5-self.id_team)*diff_x>0) and (dist_opp < zone)) :         
           if 2*(1.5-self.id_team)*diff_y < 0 : # si l'adversaire est a ma gauche je vais a droite et inversement
                dir_adv.angle += math.pi/4
           else :
               dir_adv.angle -= math.pi/4
           return SoccerAction ( shoot = dir_adv.normalize() * maxPlayerShoot /8 )
#        listeTrier = sorted( liste , key = lambda x: x[1])        
#        return listeTrier[0]    
        else :
            return self.dribbler

    @property
    def gotBall( self ):
        return self.player.distance( self.ball ) <= PLAYER_RADIUS + BALL_RADIUS
    
    @property 
    def positionnement( self ):
        if self.ball.distance(self.goal_ally) < 17 :
            return self.to_ball
        return self.move ( Vector2D( ( ( 2*self.id_team - 1  ) / 8) * GAME_WIDTH , (self.ball.y + self.goal_ally.y)/2))
              
    @property
    def team_gotBall( self ) :    #trouve l'adversaire le plus proche devant soit renvoi un tuple ( distance , id_team ) 
        return self.id_team == min([( self.ball.distance( self.state.player_state( id_team , id_player ).position ) , id_team ) for ( id_team , id_player ) in self.state.players])[1]

    @property 
    def maTeam( self ) :
        return [ self.player for self.player in self.state.players if id_team == self.id_team ]
    
    @property 
    def teamOpp( self ) :
        return [ self.player for self.player in self.state.players if id_team != self.id_team ]
    