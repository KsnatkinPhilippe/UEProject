#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:34:13 2019

@author: 3700067
"""

from soccersimulator import *

class SuperState ( object ):
    def __init__ ( self , state , id_team , id_player , dribble=.6 , force=.2):
            self.state = state
            self.id_team = id_team
            self.id_player = id_player
            self . dribble = dribble
            self . force = force

#def __getattr__ ( self , attr ):
#    return getattr ( self . state , attr )

#    def playerState( self ):
        

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
#        if(self.ball.x==GAME_WIDTH/2 and  self.ball.y==GAME_HEIGHT/2):
#        if(self.ball == Vector2D(GAME_WIDTH/2 , GAME_HEIGHT/2)):
#            return self.move(Vector2D(GAME_WIDTH/2 - 2*(1.5-self.id_team)*15, GAME_HEIGHT/2
        if self.ball.distance(self.player) < 4 :
            return self.move(self.ball)
        return self.move(5*self.state.ball.vitesse + self.ball)


    def shoot( self , cible , norme) :
        return self.to_ball + SoccerAction( shoot = ( cible - self.ball ).normalize() * norme ) 
    
    def move( self , cible ): # aller vers la cible immobile
        acceleration = cible - self.player
        acceleration.norm = settings.maxPlayerAcceleration
        return SoccerAction( acceleration )
        
    def dribbler( self , cible) : # foncer vers les buts avec le ballon
        return self.to_ball + self.shoot( cible, self.dribble )

    @property
    def tirer_au_but( self ):
#        return self.shoot( self.goal , 1/(1 + math.exp(-5*(self.ball.distance( self.goal )- 30))))
        return self.shoot( self.goal , maxPlayerShoot )


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


#fonction de tri sorted
#        listeTrier = sorted( liste , key = lambda x: x[1]) 
#        return  (listeTrier[0]) 


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
            return self.to_goal(self.force)

    @property
    def gotBall( self ):
#        if (self.state.ball.vitesse.norm == 0):
#            return self.player.distance( self.ball ) < 1.784 + PLAYER_RADIUS + BALL_RADIUS
        return self.player.distance( self.ball ) <= PLAYER_RADIUS + BALL_RADIUS + self.state.ball.vitesse.norm
    
    
    @property 
    def positionnement( self ):
        if self.ball.distance(self.goal_ally) < GAME_WIDTH/5  :
            return self.to_ball
#        return self.move ( Vector2D( (6*(self.id_team-1) + 1) / 8 * GAME_WIDTH , (self.ball.y + self.goal_ally.y)/2))
        return self.move((self.ball + self.goal_ally)/2)
              
    @property
    def team_gotBall( self ) :    #trouve l'adversaire le plus proche devant soit renvoi un tuple ( distance , id_team ) 
        return self.id_team == min([( self.ball.distance( self.state.player_state( id_team , id_player ).position ) , id_team ) for ( id_team , id_player ) in self.state.players])[1]

    @property 
    def maTeam( self ) :
        return [ ( id_team , id_player ) for ( id_team , id_player ) in self.state.players if id_team == self.id_team ]
      

    @property 
    def ciblePasse(self): #trouve le partenaire le plus libre  et renvoie un tuple (distance avec adv le plus proche , id_player  )
        return max([(SuperState(self.state, id_team , id_player).adversaire_le_plus_proche[0] , id_player ) 
            for  ( id_team , id_player )  in self.maTeam if SuperState(self.state, id_team , id_player).adversaire_le_plus_proche], default= None )

        

#    @property 
#    def passe(self):
#        if (not self.ciblePasse):
#            return self.dribbler
#        return self.shoot( self.state.player_state( self.id_team , self.ciblePasse[1]).position , 1 )
    
    @property 
    def passe(self):
        ciblePos=self.state.player_state( self.id_team , self.id_player+1).position
        
        if self.id_player==3:
            ciblePos=self.goal
        
        if self.id_player<2 and self.state.player_state( self.id_team , self.id_player+1).position.distance(self.player) < 15:
            ciblePos=self.state.player_state( self.id_team , self.id_player+2).position
        
        d=self.ball.distance(ciblePos)
        return self.shoot( ciblePos , d/9 )
    
    @property
    def attaque(self):
        if self.ball.distance(self.goal_ally) < GAME_WIDTH/2  :
            return self.move(Vector2D( GAME_WIDTH/2 , self.ball.y ))
        
        if self.gotBall : # condition si le joueur peut touche la balle
            if self.ball.distance( self.goal ) < 25 : # si la balle est dans la zone de shoot
                return self.to_goal(self.force)
            else :
                return self.avancer_en_esquivant( 30 )
        else :
            return self.to_ball
        
    @property
    def defense(self):
        if self.gotBall :
            return self.passe
        return self.positionnement
        
        
    def placerEntrePourxDef(self , x , pos1 , pos2 ): # a ameliorer
        a = (pos2.y - pos1.y)/(pos2.x - pos1.x)
        b = pos2.y - pos2.x*a
        return Vector2D( x , a*x+b )
    
    @property
    def AdvAtt( self ) :    #trouve l'adversaire le plus proche de mes buts en renvoyant un tuple ( distance au cages , Position du joueur , ( id_team, id_ player ) )
        advTuple = [( jPos.distance( self.goal_ally ) , player ) for ( jPos , player ) in self.advs ]
        return min( advTuple )
    
    def milieuAtt(self):
        return self.state.player_state ( self.id_team , 2 ).position

    @property
    def estLePlusPrès(self):
        mates= [ ( self.ball.distance(self.state.player_state( id_team , id_player ).position ) , id_player ) for ( id_team , id_player ) in self.maTeam ]
        distlProch , idProche = min(mates)
        return self.id_player == idProche