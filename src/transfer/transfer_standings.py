import os

import requests

from src.utils.constants import constants
from src.utils.DBConnection import DBConnection

def __fetch_api(competition, team_count):
    url = f"http://api.football-data.org/v4/competitions/{competition}/standings"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    standings_data = []

    for i in range(0, team_count):
        standings_data.append(
            (
                int(data["standings"][0]["table"][i]["team"]["id"]),
                int(data["competition"]["id"]),
                int(data["standings"][0]["table"][i]["position"]),
                int(data["standings"][0]["table"][i]["points"]),
                int(data["standings"][0]["table"][i]["playedGames"]),
                int(data["standings"][0]["table"][i]["won"]),
                int(data["standings"][0]["table"][i]["draw"]),
                int(data["standings"][0]["table"][i]["lost"]),
                int(data["standings"][0]["table"][i]["goalsFor"]),
                int(data["standings"][0]["table"][i]["goalsAgainst"]),
                int(data["standings"][0]["table"][i]["goalDifference"])
            )
        )
    
    return standings_data

def start_pipeline(competition, team_count):
    print("Fetching data from API ...")
    standings_data = __fetch_api(competition, team_count)
    print("Data fetched. Proceeding to create connection to Postgres ...")

    conn = DBConnection().get_connection()

    print("Connection to Postgres established. Proceeding to add data ...")

    cur = conn.cursor()

    # First we need to delete the old data
    cur.execute(f"DELETE FROM standings WHERE league_id = {competition}")

    standings_insert_query = """
                        INSERT INTO standings (
                            team_id, 
                            league_id, 
                            position, 
                            points, 
                            matches_played, 
                            wins, 
                            draws, 
                            losses, 
                            goals_for, 
                            goals_against, 
                            goal_difference
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """

    cur.executemany(standings_insert_query, standings_data)

    conn.commit()
    cur.close()
    conn.close()