"""
    Here, we will load the standings data present in our bigquery, load it into a dataframe then show the
    dataframe as a table on our streamlit application.
"""
import os

import pandas_gbq
from pandas import DataFrame
import src.constants.constants as constants
from google.oauth2 import service_account

def fetch_from_bq() -> DataFrame:
    query = """
                SELECT position, team, games_played, wins, draws, losses, points, goals_for, goals_against, goal_difference
                from bigquery_dataset1.standings
                order by position ASC
            """
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )
    df = pandas_gbq.read_gbq(
        query_or_table=query,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        credentials=credentials,
        dialect="legacy"
    )

    return df

def get_standings() -> DataFrame:
    return fetch_from_bq()