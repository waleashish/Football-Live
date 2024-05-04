import os

import requests
import psycopg2
import time

def __fetch_api(competition):
    url = f"http://api.football-data.org/v4/competitions/{competition}/scorers"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv("FOOTBALL_API_KEY")
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    top_scorers_data = []

    for i in range(0, 10):
        top_scorers_data.append(
            (
                int(data["scorers"][i]["player"]["id"]),
                str(data["scorers"][i]["player"]["name"]),
                int(data["scorers"][i]["team"]["id"]),
                int(data["scorers"][i]["goals"]),
                int(data["scorers"][i]["assists"]),
                int(data["competition"]["id"])
            )
        )
    
    return top_scorers_data

def start_pipeline(competition):
    top_scorers_data = __fetch_api(competition)
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

    # First we need to delete the old data
    cur.execute(f"DELETE FROM top_scorers WHERE league_id = 2021")

    top_scorers_insert_query = """
                        INSERT INTO top_scorers (
                            player_id, 
                            player_name, 
                            team_id, 
                            goals,
                            assists,
                            league_id
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """

    cur.executemany(top_scorers_insert_query, top_scorers_data)

    conn.commit()
    cur.close()
    conn.close()