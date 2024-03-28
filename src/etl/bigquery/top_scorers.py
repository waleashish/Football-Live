import os

import pandas_gbq
import src.utils.constants.constants as constants
from pandas import DataFrame
from google.oauth2 import service_account

def __fetch_from_bq() -> DataFrame:
    query = """
                SELECT
                name AS Name,
                team AS Team,
                goals AS Goals,
                assists AS Assists,
                matches_played AS Matches,
                nationality AS Nationality
                FROM bigquery_dataset1.top_scorers
                ORDER BY Goals DESC
            """
    
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    return pandas_gbq.read_gbq(
        query_or_table=query,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        credentials=credentials,
        dialect="legacy"
    )

def get_top_scorers() -> DataFrame:
    return __fetch_from_bq()