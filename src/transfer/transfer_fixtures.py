import os

import requests

from src.utils.constants import constants, league_name_constants
from src.utils.DBConnection import DBConnection

def __fetch_api(competition):
    url = f"http://api.football-data.org/v4/competitions/{competition}/matches"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
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
                    int(data["matches"][i]["score"]["fullTime"]["away"]) if data["matches"][i]["score"]["fullTime"]["away"] != None else None,
                    int(data["matches"][i]["matchday"])
                )
            )
        i += 1
    
    return matches_data

def start_pipeline():
    # Get connection to Postgres
    conn = DBConnection().get_connection()
    print("Connection to Postgres established. Proceeding to add data ...")
    cur = conn.cursor()

    for competition in league_name_constants.LEAGUE_IDS:

        matches_data = __fetch_api(competition)

        matches_upsert_query = """
                            INSERT INTO fixtures (
                                fixture_id,
                                home_team_id,
                                away_team_id,
                                league_id,
                                status,
                                home_team_score,
                                away_team_score,
                                matchday
                            ) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (fixture_id)
                            DO UPDATE SET
                                status = EXCLUDED.status,
                                home_team_score = EXCLUDED.home_team_score,
                                away_team_score = EXCLUDED.away_team_score
                            """

        cur.executemany(matches_upsert_query, matches_data)

    conn.commit()
    cur.close()