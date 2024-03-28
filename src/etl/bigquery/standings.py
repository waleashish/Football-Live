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
                position AS Rank,
                team AS Team,
                games_played AS Matches,
                wins AS Win,
                losses AS Lose,
                draws AS Draw,
                points AS Points,
                goal_difference AS GD,
                goals_for AS GF,
                goals_against AS GA
                FROM bigquery_dataset1.standings
                ORDER BY Rank ASC
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