import os

import requests
import pandas_gbq
import src.utils.constants.constants as constants
from pandas import DataFrame
from google.oauth2 import service_account
from dotenv import load_dotenv

def __fetch_api():
    url = "http://api.football-data.org/v4/competitions/PL/matches"
    payload = {}
    headers = {
        'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
    }
    response = requests.request("GET", url, headers=headers, params=payload)
    data = response.json()
    current_matchday = int(data["matches"][0]["season"]["currentMatchday"])

    matchday_list = []
    home_team_list = []
    away_team_list = []
    status_list = []
    scores_list = []

    i = 0
    while True:
        matchday = int(data["matches"][i]["matchday"])
        if matchday > current_matchday:
            break
        matchday_list.append(int(data["matches"][i]["matchday"]))
        home_team_list.append(str(data["matches"][i]["homeTeam"]["shortName"]))
        away_team_list.append(str(data["matches"][i]["awayTeam"]["shortName"]))
        status_list.append(str(data["matches"][i]["status"]))
        scores_list.append(str(data["matches"][i]["score"]))

        i += 1

    return (
        matchday_list,
        home_team_list,
        away_team_list,
        status_list,
        scores_list
    )


def __create_dataframe() -> DataFrame:
    print(f"Fetching Data from Football API ...")
    (
        matchday_list,
        home_team_list,
        away_team_list,
        status_list,
        scores_list
    ) = __fetch_api()

    headers = [
        "matchday",
        "home_team",
        "away_team",
        "status",
        "score"
    ]

    data_zipped = zip(
        matchday_list,
        home_team_list,
        away_team_list,
        status_list,
        scores_list
    )

    df = DataFrame(data_zipped, columns=headers)
    return df

def __define_table_schema():
    schema_definition = [
		{"name": "matchday", "type": "INTEGER"},
		{"name": "home_team", "type": "STRING"},
		{"name": "away_team", "type": "STRING"},
        {"name": "status", "type": "STRING"},
		{"name": "score", "type": "STRING"}
	]

    return schema_definition


def __add_fixtures_data_to_bigquery(dataframe, schema) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    pandas_gbq.to_gbq(
        dataframe=dataframe,
        destination_table="bigquery_dataset1.fixtures",
        if_exists="replace",
        table_schema=schema,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        credentials=credentials
    )

def start_pipeline():
    load_dotenv(dotenv_path=constants.DOTENV_PATH)
    print(f"Starting ETL pipeline ...")
    dataframe = __create_dataframe()
    schema = __define_table_schema()
    print(f"Adding fixtures data to BigQuery ...")
    __add_fixtures_data_to_bigquery(dataframe, schema)
    print(f"Addition complete")