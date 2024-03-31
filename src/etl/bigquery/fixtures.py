import os

import pandas_gbq
from google.oauth2 import service_account
from src.utils.constants import constants

def __fetch_from_bq():
    query = f"""
                SELECT * FROM 
                (SELECT matchday, short_name AS home_team_name, crest, score, away_team
                FROM bigquery_dataset1.fixtures as fix INNER JOIN bigquery_dataset1.teams AS teams
                ON fix.home_team = teams.short_name
                ORDER BY matchday DESC) AS one
                INNER JOIN
                (SELECT matchday, short_name as away_team_name, crest
                FROM bigquery_dataset1.fixtures AS fix INNER JOIN bigquery_dataset1.teams AS teams
                ON fix.away_team = teams.short_name
                ORDER BY matchday DESC) AS two
                ON one.matchday = two.matchday AND one.away_team = two.away_team_name;
            """
    
    credentials = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_PATH
    )

    df = pandas_gbq.read_gbq(
        query_or_table=query,
        credentials=credentials,
        project_id=os.getenv(constants.GCLOUD_PROJECT),
        dialect="legacy"
    )

    df = df.drop(["one_away_team", "two_matchday"], axis=1)

    return df

def get_all_fixtures():
    return __fetch_from_bq()