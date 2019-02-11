#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 18:59:40 2019

@author: 3522974
"""


from Simulation import Attaquant , Defenseur
from soccersimulator import SoccerTeam

def get_team ( nb_players ):
    team = SoccerTeam ( name = " Philippe ’s ␣ Team " )
    if nb_players == 1:
        team . add ( " Striker " , Attaquant ())
    if nb_players == 2:
        team . add ( " Striker " , Attaquant ())
        team . add ( " Blocker " , Defenseur ())
    return team


if __name__ == '__main__':
    from soccersimulator import Simulation , show_simu

    # Check teams with 1 player and 2 players
    team1 = get_team (1)
    team2 = get_team (2)

    # Create a match
    simu = Simulation ( team1 , team2 )

    # Simulate and display the match
    show_simu ( simu )