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

    @property
    def ball ( self ):
        return self.state.ball.position

    @property
    def player ( self ):
        return self.state.player_state ( self.id_team , self.id_player ).position

    @property
    def goal ( self ):
        return Vector2D( GAME_WIDTH * ( 2 - self.id_team  ), GAME_HEIGHT /2. ) #si j'enleve le vect "tuple has no attribute 'distance'" s'affiche
    
    @property
    def to_ball( self ) : #aller vers la futur position du ballon
        if self.state.ball.vitesse.norm != 0 : # vérifie que la balle bouge   
            return SoccerAction( acceleration = ( self.state.ball.vitesse.norm_max(maxBallAcceleration) + self.ball  - self.player).norm_max( maxPlayerAcceleration )) 
        return self.move( self.ball ) # Peut-etre mieux sans le faire bouger

    def shoot( self , cible , norme) :
        return SoccerAction( shoot = ( cible - self.ball ).norm_max( norme ) ) 
    
    def move( self , cible ): # aller vers la cible immobile
        return SoccerAction( acceleration = ( cible - self.player ).norm_max( maxPlayerAcceleration ) )
         
    
        
    @property #vitesse du joueur a opti
    def dribbler( self ) : # foncer vers les buts avec le ballon
        return self.shoot( self.goal , maxPlayerShoot / 5 )

    @property
    def tirer_au_but( self ):
        return self.shoot( self.goal , maxPlayerShoot)


    @property
    def adversaire_le_plus_proche( self ) :    #trouve l'adversaire le plus proche devant soit renvoi un tuple ( distance , id_ player , distance en y , id_team ) 
        return  min([( self.player.distance( self.state.player_state( id_team , id_player ).position ) ,  id_player , self.state.player_state( id_team , id_player ).position.y - self.player.y , id_team ) for ( id_team , id_player ) in self.state.players if id_team != self.id_team])



    def avancer_en_esquivant( self , zone ) :     #prend en argument la zone de souveraineté du joueur et renvoie la marche a suivre
        
        dist_opp, id_opp, dist_opp_y, id_team_opp = self.adversaire_le_plus_proche
        
        adversaire = self.state.player_state( id_team_opp , id_opp).position
        
        dir_adv = adversaire - self.ball 
        
        
#        if ( ((self.id_player-2) < math.cos(dir_adv.angle) < (self.id_player-1)) and (dist_opp < zone)) :
        if ((math.cos(dir_adv.angle) > math.cos(5*math.pi/3)) and dist_opp < zone) :     #si l'adversaire est assez proche pour etre dangeureux ou si je ne l'ai pas encore passé => change de direction   
            if dist_opp_y < 0 : # si l'adversaire est a ma gauche je vais a droite et inversement
                dir_adv.angle += math.pi/4
            else :
                dir_adv.angle -= math.pi/4
            return SoccerAction ( shoot = dir_adv.norm_max( maxPlayerShoot ) /8 )
#        listeTrier = sorted( liste , key = lambda x: x[1]) 
#        
#        return listeTrier[0]
    
        else :
            return self.dribbler

    @property
    def gotBall( self ):
        return self.player.distance( self.ball ) <= PLAYER_RADIUS + BALL_RADIUS
    
    
    @property
    def team_gotBall( self ) :    #trouve l'adversaire le plus proche devant soit renvoi un tuple ( distance , id_team ) 
        return self.id_team == min([( self.ball.distance( self.state.player_state( id_team , id_player ).position ) , id_team ) for ( id_team , id_player ) in self.state.players])[1]

    @property 
    def maTeam( self ) :
        return [ self.player for self.player in self.state.players if id_team == self.id_team ]
    
    @property 
    def teamOpp( self ) :
        return [ self.player for self.player in self.state.players if id_team != self.id_team ]
    
    @property
    def se_replacer( self ) :
        return self.move ( Vector2D( ( ( 2*self.id_team - 1  ) / 4) * GAME_WIDTH , GAME_HEIGHT/2 ) )