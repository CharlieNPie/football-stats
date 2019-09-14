#Indicates which teams are over-achieving and under-achieving in the league. 

#main package
from understat import Understat

#JSON and async packages
import json
import asyncio

#async http
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_teams(
            "epl", 2019
        )

        #get team name and match data from table
        team_names = [team["title"] for team in results]
        team_history_dict = [team["history"] for team in results]
        match_history_dict = [match for match in team_history_dict]

        overachievers = []
        underachievers = []
        

        #sort teams and calculate full xPts for each
        for i in range(len(team_names)):

            #get team name
            team_name = team_names[i]

            #extract fixture history
            team_fixture_history = match_history_dict[i]

            #get expected point total
            x_pts = sum([fixture["xpts"] for fixture in team_fixture_history])

            #get actual point total
            real_pts = sum([fixture["pts"] for fixture in team_fixture_history])

            pt_difference = real_pts - x_pts
        
            if pt_difference > 1:
                overachievers.append(team_name)
            elif pt_difference < -1:
                underachievers.append(team_name)
                
        overachievers.sort()
        underachievers.sort()

        return (overachievers, underachievers)

def get_data():
    loop = asyncio.get_event_loop()
    over_under_tuple = loop.run_until_complete(main())
    return over_under_tuple

