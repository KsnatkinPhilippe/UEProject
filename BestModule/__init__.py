#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:31:34 2019

@author: 3522974
"""
from .Strategies import Attaquant , Defenseur , MilieuDef , MilieuAtt
from soccersimulator import SoccerTeam

def get_team ( nb_players ):
    team = SoccerTeam ( name = "Team zigzaton " )
    if nb_players == 1:
#        team . add ( " Striker " , Attaquant ())
#        team . add ( " Blocker " , Test ())
        team . add ( " Clifford Hume " , Defenseur ()) 
    if nb_players == 2:
        team . add ( " Striker " , Attaquant ())
        team . add ( " Blocker " , Defenseur ())
    if nb_players == 4:
        team . add ( " Clifford Hume " , Defenseur ())
        team . add ( " Ben Becker " , MilieuDef ())
        team . add ( " Olivier Atton " , MilieuAtt())
        team . add ( " Mark Landers " , Attaquant ())
    return team

