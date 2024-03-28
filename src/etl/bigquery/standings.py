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

def __fetch_from_bq() -> DataFrame:
    query = """
                SELECT 
                position,
                crest,
                team,
                games_played,
                wins,
                losses,
                draws,
                points,
                goal_difference,
                goals_for,
                goals_against
                FROM bigquery_dataset1.standings INNER JOIN bigquery_dataset1.teams
                ON bigquery_dataset1.standings.team = bigquery_dataset1.teams.short_name
                ORDER BY position ASC
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
    return __fetch_from_bq()