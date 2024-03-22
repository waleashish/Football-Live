"""
    Load data into bigquery. This should be done every once a week to regularly update the matchday
    standings. On any off weekend matchday, we should have a trigger to start the pipeline to update the
    standings for an updated table.
"""
import os

import requests
import pandas_gbq
import src.constants.constants as constants
from pandas import DataFrame
from google.oauth2 import service_account

def fetch_api():
    url = "http://api.football-data.org/v4/competitions/PL/standings"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    positions = []
    teams = []
    games_played_list = []
    wins_list = []
    draws_list = []
    losses_list = []
    points_list = []
    goals_for_list = []
    goals_against_list = []
    goal_difference_list = []

    for i in range(0, 20):
        positions.append(int(data["standings"][0]["table"][i]["position"]))
        teams.append(str(data["standings"][0]["table"][i]["team"]["shortName"]))
        games_played_list.append(int(data["standings"][0]["table"][i]["playedGames"]))
        wins_list.append(int(data["standings"][0]["table"][i]["won"]))
        draws_list.append(int(data["standings"][0]["table"][i]["draw"]))
        losses_list.append(int(data["standings"][0]["table"][i]["lost"]))
        points_list.append(int(data["standings"][0]["table"][i]["points"]))
        goals_for_list.append(int(data["standings"][0]["table"][i]["goalsFor"]))
        goals_against_list.append(int(data["standings"][0]["table"][i]["goalsAgainst"]))
        goal_difference_list.append(int(data["standings"][0]["table"][i]["goalDifference"]))

    return (
        positions,
        teams,
        games_played_list,
        wins_list,
        draws_list,
        losses_list,
        points_list,
        goals_for_list,
        goals_against_list,
        goal_difference_list
    )


def create_dataframe() -> DataFrame:
    print(f"Fetching Data from Football API ...")
    (
        positions,
        teams,
        games_played_list,
        wins_list,
        draws_list,
        losses_list,
        points_list,
        goals_for_list,
        goals_against_list,
        goal_difference_list
    ) = fetch_api()

    headers = [
        "position",
        "team",
        "games_played",
        "wins",
        "draws",
        "losses",
        "points",
        "goals_for",
        "goals_against",
        "goal_difference"
    ]

    data_zipped = zip(
        positions,
        teams,
        games_played_list,
        wins_list,
        draws_list,
        losses_list,
        points_list,
        goals_for_list,
        goals_against_list,
        goal_difference_list
    )

    df = DataFrame(data_zipped, columns=headers)
    return df

def define_table_schema() -> list[dict[str, str]]:
    schema_definition = [
		{"name": "position", "type": "INTEGER"},
		{"name": "team", "type": "STRING"},
		{"name": "games_played", "type": "INTEGER"},
		{"name": "wins", "type": "INTEGER"},
		{"name": "draws", "type": "INTEGER"},
		{"name": "loses", "type": "INTEGER"},
		{"name": "points", "type": "INTEGER"},
		{"name": "goals_for", "type": "INTEGER"},
		{"name": "goals_against", "type": "INTEGER"},
		{"name": "goal_difference", "type": "INTEGER"},
	]

    return schema_definition


def add_standings_data_to_bigquery(dataframe, schema) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    pandas_gbq.to_gbq(
        dataframe=dataframe,
        destination_table="bigquery_dataset1.standings",
        if_exists="replace",
        table_schema=schema,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        credentials=credentials
    )
    

def start_pipeline():
    print(f"Starting ETL pipeline ...")
    dataframe = create_dataframe()
    schema = define_table_schema()
    print(f"Adding data to BigQuery ...")
    add_standings_data_to_bigquery(dataframe, schema)
    print(f"Addition complete")