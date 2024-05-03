import os
import requests
import psycopg2
import time

def __fetch_api(competition, team_count):
    url = f"http://api.football-data.org/v4/competitions/{competition}/teams"
    payload = {}
    headers = {
       'X-Auth-Token': os.getenv("FOOTBALL_API_KEY")
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    print("Fetching complete")

    seed_data = []

    for i in range(0, team_count):
        seed_data.append(
            (
                int(data["teams"][i]["id"]),
                str(data["teams"][i]["name"]),
                str(data["teams"][i]["crest"]),
                str(data["teams"][i]["venue"]),
                str(data["competition"]["id"])
            )
        )
    
    return seed_data

if __name__=="__main__":
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

    print("Connection to Postgres established. Proceeding with seeding data ...")

    cur = conn.cursor()

    competition_codes = [("PL", 20), ("PD", 20), ("SA", 20), ("BL1", 18), ("FL1", 18)]
    for (competition, team_count) in competition_codes:
        teams_seed_data = __fetch_api(competition, team_count)
        teams_insert_query = "INSERT INTO teams (team_id, name, crest, venue, league_id) VALUES (%s, %s, %s, %s, %s)"

        cur.executemany(teams_insert_query, teams_seed_data)

    conn.commit()
    cur.close()
    conn.close()
