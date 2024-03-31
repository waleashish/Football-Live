import os

import requests
import pandas_gbq
import src.utils.constants.constants as constants
from pandas import DataFrame
from google.oauth2 import service_account
from dotenv import load_dotenv


def __fetch_api():
    url = "http://api.football-data.org/v4/competitions/PL/scorers"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    print("Fetching complete")

    names_list = []
    teams_list = []
    goals_list = []
    assists_list = []
    matches_played = []
    nationality_list = []

    for i in range(0, 10):
        names_list.append(str(data["scorers"][i]["player"]["name"]))
        teams_list.append(str(data["scorers"][i]["team"]["shortName"]))
        goals_list.append(int(data["scorers"][i]["goals"]))
        assists_list.append(int(data["scorers"][i]["assists"] or 0))
        matches_played.append(int(data["scorers"][i]["playedMatches"]))
        nationality_list.append(str(data["scorers"][i]["player"]["nationality"]))
    
    return (
        names_list,
        teams_list,
        goals_list,
        assists_list,
        matches_played,
        nationality_list
    )

def __create_dataframe() -> DataFrame:
    (
        names_list,
        teams_list,
        goals_list,
        assists_list,
        matches_played,
        nationality_list
    ) = __fetch_api()

    headers = [
        "name",
        "team",
        "goals",
        "assists",
        "matches_played",
        "nationality"
    ]

    data_zipped = zip(
        names_list,
        teams_list,
        goals_list,
        assists_list,
        matches_played,
        nationality_list
    )

    df = DataFrame(data_zipped, columns=headers)

    return df

def __define_table_schema():
    schema_definition = [
        {"name": "name", "type": "STRING"},
        {"name": "team", "type": "STRING"},
        {"name": "goals", "type": "INTEGER"},
        {"name": "assists", "type": "INTEGER"},
        {"name": "matches_played", "type": "INTEGER"},
        {"name": "nationality", "type": "STRING"},
    ]

    return schema_definition

def __add_top_scorers_data_to_bigquery(dataframe, schema) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    pandas_gbq.to_gbq(
        dataframe=dataframe,
        credentials=credentials,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        table_schema=schema,
        if_exists="replace",
        destination_table="bigquery_dataset1.top_scorers"
    )

def start_pipeline():
    print("Fetching top scorer data from api ...")
    load_dotenv(dotenv_path=constants.DOTENV_PATH)
    print(f"Starting ETL pipeline ...")
    dataframe = __create_dataframe()
    schema = __define_table_schema()
    print(f"Adding top scorers data to BigQuery ...")
    __add_top_scorers_data_to_bigquery(dataframe, schema)
    print(f"Addition complete")