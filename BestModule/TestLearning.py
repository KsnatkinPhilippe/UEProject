#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:53:11 2019

@author:  3522974
"""

from learning import QLearning , QStrategy

# Strategy
QTestStrategy = QStrategy ()
#QTestStrategy . add ( ' right ' , Strategy ( shoot_right , ' ' ))
#QTestStrategy . add ( ' left ' , Strategy ( shoot_left , ' ' ))
#QTestStrategy . add ( ' up ' , Strategy ( shoot_up , ' ' ))
#QTestStrategy . add ( ' down ' , Strategy ( shoot_down , ' ' ))

QTestStrategy . add ( ' attaque ' , Attaquant ( ))
QTestStrategy . add ( ' attaque ' , Defenseur ( ))

# Learning
expe = QLearning ( strategy = QTestStrategy , monte_carlo = False )
expe . start ( fps =1500)

with open ( 'qstrategy.pkl' , 'wb') as fo :
    QTestStrategy . qtable = expe . qtable
    pkl . dump ( QTestStrategy , fo )

# Test
with open ( 'qstrategy.pkl.351' , 'rb') as fi :
    QStrategy = pkl . load ( fi )

    # Simulate and display the match
#    simu = RandomPos ( QStrategy )
    simu . start ()