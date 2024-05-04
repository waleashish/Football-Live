import os

import requests
import psycopg2
import src.utils.constants.constants as constants

def __fetch_api(competition, team_count):
    url = f"http://api.football-data.org/v4/competitions/{competition}/standings"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv("FOOTBALL_API_KEY")
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
    standings_data = __fetch_api(competition, team_count)
    while True:
        try:
            conn = psycopg2.connect(
                dbname="football",
                user="football",
                password="football",
                host="postgres-football"
            )
            break

        except psycopg2.OperationalError:
            time.sleep(1)

    print("Connection to Postgres established. Proceeding to add data ...")

    cur = conn.cursor()

    teams_seed_data = __fetch_api(competition, team_count)
    teams_insert_query = """
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

    cur.executemany(teams_insert_query, teams_seed_data)

    conn.commit()
    cur.close()
    conn.close()