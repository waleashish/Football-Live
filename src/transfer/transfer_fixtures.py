import os

import requests
import psycopg2
import time

from src.utils.constants import league_name_constants

def __fetch_api(competition):
    url = f"http://api.football-data.org/v4/competitions/{competition}/matches"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv("FOOTBALL_API_KEY")
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    matches_data = []
    i = 0

    current_matchday = int(data["matches"][0]["season"]["currentMatchday"])
    fixtures_count = int(data["resultSet"]["count"])
    
    while i < fixtures_count:
        matchday = int(data["matches"][i]["matchday"])
        if matchday == current_matchday:
            matches_data.append(
                (
                    int(data["matches"][i]["id"]),
                    int(data["matches"][i]["homeTeam"]["id"]),
                    int(data["matches"][i]["awayTeam"]["id"]),
                    int(data["competition"]["id"]),
                    str(data["matches"][i]["status"]),
                    int(data["matches"][i]["score"]["fullTime"]["home"]) if data["matches"][i]["score"]["fullTime"]["home"] != None else None,
                    int(data["matches"][i]["score"]["fullTime"]["away"]) if data["matches"][i]["score"]["fullTime"]["away"] != None else None
                )
            )
        i += 1
    
    return matches_data

def start_pipeline():
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

    for competition in league_name_constants.LEAGUE_IDS:

        matches_data = __fetch_api(competition)

        matches_insert_query = """
                            INSERT INTO fixtures (
                                fixture_id,
                                home_team_id,
                                away_team_id,
                                league_id,
                                status,
                                home_team_score,
                                away_team_score
                            ) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """

        cur.executemany(matches_insert_query, matches_data)

    conn.commit()
    cur.close()
    conn.close()