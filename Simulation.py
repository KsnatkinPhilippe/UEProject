#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:59:17 2019

@author: 3700067
"""

#
from BestModule import*
#from soccersimulator import Simulation, show_simu
from soccersimulator import*
from Test import *


# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
#team1.add("Principal", GoTestStrategy())  
#team1.add("Principal", Attaquant())  
#team2.add("Static", Defenseur())   
team2.add("Principal2", Attaquant())
team1.add("Static2", Defenseur())
# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
