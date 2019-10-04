#stats package
from understat import Understat

#JSON and async packages
import json
import asyncio
import aiohttp

#Maths packages
import math
import numpy as np


# ---------------- HOMEPAGE ---------------------------------

#gets match data for every team in EPL
async def fixture_data():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_teams(
            "epl", 2019
        )
    return results


#gets all data for teams, including names and match history
def get_team_data():
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fixture_data())

    #get team name and match data from table
    team_names = [team["title"] for team in results]
    team_history_dict = [team["history"] for team in results]
    match_history_dict = [match for match in team_history_dict]

    return (team_names, match_history_dict)

#compiles expected points for every team and classes them as over/underachieving
def get_xpts():

    #get team data from helper function
    (team_names, match_history_dict) = get_team_data()

    #empty lists for over/underachievers
    overachievers = []
    underachievers = []

    #sort teams and calculate full xPts for each
    for i in range(len(team_names)):

        #get team name
        team_name = team_names[i]

        #extract fixture history
        team_fixture_history = match_history_dict[i]

        #list of expected point values
        x_pts = [fixture["xpts"] for fixture in team_fixture_history]
        x_pts_total = sum(x_pts)

        #get actual point total
        real_pts_total = sum([fixture["pts"] for fixture in team_fixture_history])

        #difference in real and expected points 
        pt_difference = real_pts_total - x_pts_total

        #compute chi-squared value 
        chi_squared_points = (pt_difference**2)/x_pts_total
    
        #append to over/underachievers
        if chi_squared_points > 0.5:
            if pt_difference > 0:
                overachievers.append((team_name, '%.3f'%(pt_difference)))
            elif pt_difference < 0:
                underachievers.append((team_name, '%.3f'%(pt_difference)))
            
    overachievers.sort(key=lambda x: x[1], reverse=True)
    underachievers.sort(key=lambda x: x[1], reverse=True)

    return (overachievers, underachievers)


#calculate which teams are clinical/wasteful in attack
def get_xgoals():

    #get team info from helper function
    (team_names, match_history_dict) = get_team_data()
    
    #empty lists for over/underachievers
    clinical = []
    wasteful = []

    #sort teams and calculate full xPts for each
    for i in range(len(team_names)):

        #get team name
        team_name = team_names[i]

        #extract fixture history
        team_fixture_history = match_history_dict[i]

        x_goals_total = sum([fixture["xG"] for fixture in team_fixture_history])
        real_goals_total = sum([fixture["scored"] for fixture in team_fixture_history])
        
        goals_difference = real_goals_total - x_goals_total

        #compute chi-squared value 
        chi_squared_goals = (goals_difference**2)/x_goals_total

        #append to over/underachievers if chi-squared exceeds critical value
        if chi_squared_goals > 0.4:
            if goals_difference > 0:
                clinical.append((team_name, '%.3f'%(goals_difference)))
            elif goals_difference < 0:
                wasteful.append((team_name, '%.3f'%(goals_difference)))

    clinical.sort(key=lambda x: x[1], reverse=True)
    wasteful.sort(key=lambda x: x[1], reverse=True)

    return (clinical, wasteful)

# Functionality for expected goals against
def get_xgoals_against():

    #get team info from helper function
    (team_names, match_history_dict) = get_team_data()
    
    #empty lists for over/underachievers
    overachievers = []
    underachievers = []

    for i in range(len(team_names)):

        #get team name
        team_name = team_names[i]

        #extract fixture history
        team_fixture_history = match_history_dict[i]

        x_goals_total = sum([fixture["xGA"] for fixture in team_fixture_history])
        real_goals_total = sum([fixture["missed"] for fixture in team_fixture_history])
        
        goals_difference = real_goals_total - x_goals_total

        #compute chi-squared value 
        chi_squared_goals = (goals_difference**2)/x_goals_total

        #append to over/underachievers if chi-squared exceeds critical value
        if chi_squared_goals > 0.4:
            if goals_difference > 0:
                overachievers.append((team_name, '%.3f'%(goals_difference)))
            elif goals_difference < 0:
                underachievers.append((team_name, '%.3f'%(goals_difference)))


    overachievers.sort(key=lambda x: x[1], reverse=True)
    underachievers.sort(key=lambda x: x[1], reverse=True)

    return(overachievers, underachievers)

# ------------------------- TEAM PAGES -----------------------------

async def results(team_name):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        fixtures = await understat.get_team_results(
            team_name,
            2019
        )
        return fixtures

def get_all_results_data():
    team_names = get_team_data()[0]

    all_team_data = {}

    for team_name in team_names:
        loop = asyncio.get_event_loop()
        team_data = loop.run_until_complete(results(team_name))
        all_team_data[team_name] = team_data

    return all_team_data


