import os
import requests
import psycopg2
import time

def __fetch_teams_data(competition, team_count):
    url = f"http://api.football-data.org/v4/competitions/{competition}/teams"
    payload = {}
    headers = {
       'X-Auth-Token': os.getenv("FOOTBALL_API_KEY")
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

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

def __fetch_fixtures_data(competition):
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
        if matchday <= current_matchday:
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

def __fetch_top_scorers_data(competition):
    url = f"http://api.football-data.org/v4/competitions/{competition}/scorers"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv("FOOTBALL_API_KEY")
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    top_scorers_data = []
    i = 0

    while i < data["count"]:
        top_scorers_data.append(
            (
                int(data["scorers"][i]["player"]["id"]),
                str(data["scorers"][i]["player"]["name"]),
                int(data["scorers"][i]["team"]["id"]),
                int(data["scorers"][i]["goals"]),
                int(data["scorers"][i]["assists"]) if data["scorers"][i]["assists"] != None else 0,
                int(data["competition"]["id"])
            )
        )
        i += 1
    
    return top_scorers_data

def __fetch_standings_data(competition, team_count):
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
            print("Connection to Postgres failed. Retrying in 1 second ...")
            time.sleep(1)

    print("Connection to Postgres established. Proceeding with seeding data ...")

    cur = conn.cursor()

    competition_codes = [("PL", 20), ("PD", 20), ("SA", 20), ("BL1", 18), ("FL1", 18)]
    print("Fetching teams data ...")
    for (competition, team_count) in competition_codes:
        teams_seed_data = __fetch_teams_data(competition, team_count)
        teams_insert_query = """
            INSERT INTO teams 
            (team_id, name, crest, venue, league_id) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.executemany(teams_insert_query, teams_seed_data)

    print("Teams data seeded successfully.")

    print("Waiting for 60 seconds before fetching fixtures data ...")
    time.sleep(60)
    print("Fetching fixtures data ...")

    for (competition, _) in competition_codes:
        fixtures_seed_data = __fetch_fixtures_data(competition)
        fixtures_insert_query = """
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
        """
        cur.executemany(fixtures_insert_query, fixtures_seed_data)

    print("Fixtures data seeded successfully.")

    print("Waiting for 60 seconds before fetching top scorers data ...")
    time.sleep(60)
    print("Fetching top scorers data ...")

    for (competition, _) in competition_codes:
        top_scorers_seed_data = __fetch_top_scorers_data(competition)
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
        cur.executemany(top_scorers_insert_query, top_scorers_seed_data)

    print("Top scorers data seeded successfully.")

    print("Waiting for 60 seconds before fetching standings data ...")
    time.sleep(60)
    print("Fetching standings data ...")

    for (competition, team_count) in competition_codes:
        standings_seed_data = __fetch_standings_data(competition, team_count)
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
        cur.executemany(standings_insert_query, standings_seed_data)

    print("Standings data seeded successfully.")
    
    print("Seeding complete. Closing connection ...")
    conn.commit()
    cur.close()
    conn.close()
    print("Connection closed.")