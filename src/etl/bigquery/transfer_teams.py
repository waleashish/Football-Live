import os

import requests
import pandas_gbq
import src.utils.constants.constants as constants
from pandas import DataFrame
from google.oauth2 import service_account
from dotenv import load_dotenv


def __fetch_api(competition):
    url = f"http://api.football-data.org/v4/competitions/{competition}/teams"
    payload = {}
    headers = {
      'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    print("Fetching complete")

    teams_list = []
    short_name_list = []
    tlas_list = []
    crests_list = []
    homes_list = []
    competition_codes_list = []

    for i in range(0, 20):
        teams_list.append(str(data["teams"][i]["name"]))
        short_name_list.append(str(data["teams"][i]["shortName"]))
        tlas_list.append(str(data["teams"][i]["tla"]))
        crests_list.append(str(data["teams"][i]["crest"]))
        homes_list.append(str(data["teams"][i]["venue"]))
        competition_codes_list.append(str(data["competition"]["code"]))
    
    return (
        teams_list,
        short_name_list,
        tlas_list,
        crests_list,
        homes_list,
        competition_codes_list
    )

def __create_dataframe(competition) -> DataFrame:
    (
        teams_list,
        short_name_list,
        tlas_list,
        crests_list,
        homes_list,
        competition_codes_list
    ) = __fetch_api(competition)

    headers = [
        "name",
        "short_name",
        "tla",
        "crest",
        "home",
        "competition_code"
    ]

    data_zipped = zip(
        teams_list,
        short_name_list,
        tlas_list,
        crests_list,
        homes_list,
        competition_codes_list
    )

    df = DataFrame(data_zipped, columns=headers)

    return df

def __define_table_schema():
    schema_definition = [
        {"name": "name", "type": "STRING"},
        {"name": "short_name", "type": "STRING"},
        {"name": "tla", "type": "STRING"},
        {"name": "crest", "type": "STRING"},
        {"name": "home", "type": "STRING"},
        {"name": "competition_code", "type": "STRING"}
    ]

    return schema_definition

def __add_standings_data_to_bigquery(dataframe, schema) -> None:
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    pandas_gbq.to_gbq(
        dataframe=dataframe,
        credentials=credentials,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        table_schema=schema,
        if_exists="append",
        destination_table="footballapp.teams"
    )

def start_pipeline(competitions):
    load_dotenv(dotenv_path=constants.DOTENV_PATH)
    print(f"Starting ETL pipeline ...")
    for competition in competitions:
        dataframe = __create_dataframe(competition)
        schema = __define_table_schema()
        print(f"Adding teams data to BigQuery ...")
        __add_standings_data_to_bigquery(dataframe, schema)
    print(f"Addition complete")