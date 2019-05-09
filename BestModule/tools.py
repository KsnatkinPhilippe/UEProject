#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:34:13 2019

@author: 3700067
"""

from soccersimulator import *

class SuperState ( object ):
    def __init__ ( self , state , id_team , id_player , dribble=.7 , force=.2):
            self.state = state
            self.id_team = id_team
            self.id_player = id_player
            self . dribble = dribble
            self . force = force

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

        if self.ball.distance(self.player) < 3 :
            return self.move(self.state.ball.vitesse + self.ball)
        return self.move(5*self.state.ball.vitesse + self.ball)


    def shoot( self , cible , norme) :
        return self.to_ball + SoccerAction( shoot = ( cible - self.ball ).normalize() * norme ) 
    
    def move( self , cible ): # aller vers la cible immobile
        acceleration = cible - self.player
        acceleration.norm = settings.maxPlayerAcceleration
        return SoccerAction( acceleration )
        
    def dribbler( self , cible) : # foncer vers les buts avec le ballon
        return self.to_ball + self.shoot( cible, self.dribble )


    def to_goal( self , norme):
        return self.shoot( self.goal , norme)

    @property
    def advs(self): #renvoie tuple (position du joueur , (id team , id player))
        return [ (self.state.player_state( id_team , id_player ).position , ( id_team , id_player )) for ( id_team , id_player ) in self.state.players if id_team != self.id_team ]

    @property
    def adversaire_le_plus_proche( self ) :    #trouve l'adversaire le plus proche devant soit renvoi un tuple ( distance , (différence en x , différence en y) , ( id_team, id_ player ) )
        advTuple = [( joueur.distance( self.player ) , (joueur.x - self.player.x , joueur.y - self.player.y ) , player )
                    for ( joueur , player ) in self.advs if (2*(1.5-self.id_team)*(self.player.x-joueur.x)<=0)]
        return min( advTuple , default=None)
    
    @property
    def adversaire_le_plus_proche_cercle( self ) :    #trouve l'adversaire le plus proche devant soit renvoi un tuple ( distance , (différence en x , différence en y) , ( id_team, id_ player ) )
        advTuple = [( joueur.distance( self.player ) , (joueur.x - self.player.x , joueur.y - self.player.y ) , player ) 
                    for ( joueur , player ) in self.advs]
        return min( advTuple , default=None)


    def avancer_en_esquivant( self , zone ) :     #prend en argument la zone de souveraineté du joueur et renvoie la marche a suivre
        
        if (self.adversaire_le_plus_proche):
            
            dist_opp, (diff_x, diff_y), (id_team_opp, id_opp) = self.adversaire_le_plus_proche        
            adversaire = self.state.player_state( id_team_opp , id_opp).position        
            dir_adv = adversaire - self.ball 

            if ((2*(1.5-self.id_team)*diff_x>0) and (dist_opp < zone)) :         
                if 2*(1.5-self.id_team)*diff_y   < 0 : # si l'adversaire est a ma gauche je vais a droite et inversement
                    dir_adv.angle += math.pi/6
                else :
                    dir_adv.angle -= math.pi/6
                return self.to_ball + SoccerAction ( shoot = dir_adv.normalize() * self.dribble )          
            else :
                return self.dribbler(self.goal)
        else :
            return self.passe
        
    @property
    def gotBall( self ):
        return self.player.distance( self.ball ) <= PLAYER_RADIUS + BALL_RADIUS + self.state.ball.vitesse.norm

    @property 
    def maTeam( self ) :
        return [ ( id_team , id_player ) for ( id_team , id_player ) in self.state.players if id_team == self.id_team ]
    
    @property 
    def passe(self):
        ciblePos=self.goal
        
        if self.id_player<3:
            ciblePos=self.state.player_state( self.id_team , self.id_player+1).position
        
        if self.id_player<2 and self.state.player_state( self.id_team , self.id_player+1).position.distance(self.player) < 15:
            ciblePos=self.state.player_state( self.id_team , self.id_player+2).position
        
        dist_opp, diff_xy , player_opp= self.adversaire_le_plus_proche_cercle
        if dist_opp > 25:
            return self.shoot(ciblePos , .3)
        
        d=self.ball.distance(ciblePos)
        if d < 10 and self.id_player==3:
            return self.shoot( ciblePos , 2 )
        
        return self.shoot( ciblePos , d/11 )
        
        
    def placerEntrePourxDef(self , x , pos1 , pos2 ): # a ameliorer
        a = (pos2.y - pos1.y)/(pos2.x - pos1.x)
        b = pos2.y - pos2.x*a
        return Vector2D( x , a*x+b )
    
    @property
    def AdvAtt( self ) :    #trouve l'adversaire le plus proche de mes buts en renvoyant un tuple ( distance au cages , Position du joueur , ( id_team, id_ player ) )
        advTuple = [( jPos.distance( self.goal_ally ) , player ) for ( jPos , player ) in self.advs ]
        return min( advTuple )

    @property
    def estLePlusPrès(self):
        mates= [ ( self.ball.distance(self.state.player_state( id_team , id_player ).position ) , id_player ) for ( id_team , id_player ) in self.maTeam ]
        distlProch , idProche = min(mates)
        return self.id_player == idProche