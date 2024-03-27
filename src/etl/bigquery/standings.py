"""
    Here, we will load the standings data present in our bigquery, load it into a dataframe then show the
    dataframe as a table on our streamlit application.

    TODO: We need to orchestrate this script so it in every 7 days to get the updated standings
"""
import os

import pandas_gbq
from pandas import DataFrame
import src.utils.constants.constants as constants
from google.oauth2 import service_account

def fetch_from_bq() -> DataFrame:
    query = """
                SELECT position, team, games_played, wins, draws, losses, points, goal_difference, goals_for, goals_against
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