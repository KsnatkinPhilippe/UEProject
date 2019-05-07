#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:31:34 2019

@author: 3522974
"""
from .Strategies import Attaquant , Defenseur , Goal , MilieuDef , MilieuAtt, Test
from soccersimulator import SoccerTeam

def get_team ( nb_players ):
    team = SoccerTeam ( name = " Philippe ’s ␣ Team " )
    if nb_players == 1:
#        team . add ( " Striker " , Attaquant ())
        team . add ( " Blocker " , Test ()) 
    if nb_players == 2:
        team . add ( " Striker " , Attaquant ())
        team . add ( " Blocker " , Defenseur ())
    if nb_players == 4:
        team . add ( " defenseur " , Defenseur ())
        team . add ( " milieudef " , MilieuDef ())
        team . add ( " milieuatt " , MilieuAtt())
        team . add ( " attaquant " , Attaquant ())
    return team

