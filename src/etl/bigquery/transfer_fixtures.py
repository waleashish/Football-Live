import os

import requests
import pandas_gbq
import src.utils.constants.constants as constants
from pandas import DataFrame
from google.oauth2 import service_account
from dotenv import load_dotenv

def __fetch_api(competition):
    url = f"http://api.football-data.org/v4/competitions/{competition}/matches"
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
    ft_scores_list = []
    ht_scores_list = []

    i = 0
    while True:
        matchday = int(data["matches"][i]["matchday"])
        if matchday > current_matchday:
            break
        matchday_list.append(int(data["matches"][i]["matchday"]))
        home_team_list.append(str(data["matches"][i]["homeTeam"]["shortName"]))
        away_team_list.append(str(data["matches"][i]["awayTeam"]["shortName"]))
        status_list.append(str(data["matches"][i]["status"]))
        home_full_time_score = str(data["matches"][i]["score"]["fullTime"]["home"]) if data["matches"][i]["score"]["fullTime"]["home"] != None else "-"
        away_full_time_score = str(data["matches"][i]["score"]["fullTime"]["away"]) if data["matches"][i]["score"]["fullTime"]["away"] != None else "-"
        ft_scores_list.append(str(home_full_time_score + " : " + away_full_time_score))
        home_half_time_score = str(data["matches"][i]["score"]["halfTime"]["home"]) if data["matches"][i]["score"]["halfTime"]["home"] != None else "-"
        away_half_time_score = str(data["matches"][i]["score"]["halfTime"]["away"]) if data["matches"][i]["score"]["halfTime"]["away"] != None else "-"
        ht_scores_list.append(str(home_half_time_score + " : " + away_half_time_score))

        i += 1

    return (
        matchday_list,
        home_team_list,
        away_team_list,
        status_list,
        ft_scores_list,
        ht_scores_list
    )


def __create_dataframe(competition) -> DataFrame:
    print(f"Fetching Data from Football API ...")
    (
        matchday_list,
        home_team_list,
        away_team_list,
        status_list,
        ft_scores_list,
        ht_scores_list
    ) = __fetch_api(competition)

    headers = [
        "matchday",
        "home_team",
        "away_team",
        "status",
        "full_time_score",
        "half_time_score"
    ]

    data_zipped = zip(
        matchday_list,
        home_team_list,
        away_team_list,
        status_list,
        ft_scores_list,
        ht_scores_list
    )

    df = DataFrame(data_zipped, columns=headers)
    return df

def __define_table_schema():
    schema_definition = [
		{"name": "matchday", "type": "INTEGER"},
		{"name": "home_team", "type": "STRING"},
		{"name": "away_team", "type": "STRING"},
        {"name": "status", "type": "STRING"},
		{"name": "full_time_score", "type": "STRING"},
        {"name": "half_time_score", "type": "STRING"}
	]

    return schema_definition


def __add_fixtures_data_to_bigquery(dataframe, schema) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    pandas_gbq.to_gbq(
        dataframe=dataframe,
        destination_table="footballapp.fixtures",
        if_exists="append",
        table_schema=schema,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        credentials=credentials
    )

def start_pipeline(competitions):
    load_dotenv(dotenv_path=constants.DOTENV_PATH)
    print(f"Starting ETL pipeline ...")
    for competition in competitions:
        dataframe = __create_dataframe(competition)
        schema = __define_table_schema()
        print(f"Adding fixtures data to BigQuery ...")
        __add_fixtures_data_to_bigquery(dataframe, schema)
    print(f"Addition complete")