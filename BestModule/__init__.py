#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:31:34 2019

@author: 3522974
"""
from .Strategies import Attaquant , Defenseur , Goal
from soccersimulator import SoccerTeam

def get_team ( nb_players ):
    team = SoccerTeam ( name = " Philippe ’s ␣ Team " )
    if nb_players == 1:
        team . add ( " Striker " , Attaquant ())
    if nb_players == 2:
        team . add ( " Striker " , Attaquant ())
        team . add ( " Blocker " , Defenseur ())
    if nb_players == 4:
        team . add ( " Striker " , Attaquant ())
        team . add ( " Striker2 " , Attaquant ())
        team . add ( " Blocker " , Defenseur ())
        team . add ( " Goal " , Goal ())
    return team

