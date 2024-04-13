import os

import pandas_gbq
import src.utils.constants.constants as constants
from pandas import DataFrame
from google.oauth2 import service_account

def __fetch_from_bq(competition) -> DataFrame:
    query = f"""
                SELECT name, team, goals, assists, matches_played, nationality, competition_code
                FROM footballapp.top_scorers
                WHERE competition_code = '{competition}'
                ORDER BY goals DESC"""

    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    df = pandas_gbq.read_gbq(
        query_or_table=query,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        credentials=credentials,
        dialect="legacy"
    )

    df = df.drop(["competition_code"], axis=1)

    return df

def get_top_scorers(competition) -> DataFrame:
    return __fetch_from_bq(competition)