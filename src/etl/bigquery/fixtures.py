import os

import pandas_gbq
from google.oauth2 import service_account
from src.utils.constants import constants

def __fetch_from_bq(competition):
    query = f"""
                SELECT * FROM 
                (SELECT matchday, short_name AS home_team_name, crest, full_time_score, half_time_score, away_team
                FROM footballapp.fixtures as fix INNER JOIN footballapp.teams AS teams
                ON fix.home_team = teams.short_name
                ORDER BY matchday DESC) AS one
                INNER JOIN
                (SELECT matchday, short_name as away_team_name, crest
                FROM footballapp.fixtures AS fix INNER JOIN footballapp.teams AS teams
                ON fix.away_team = teams.short_name
                WHERE teams.competition_code = '{competition}'
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

def get_all_fixtures(competition):
    return __fetch_from_bq(competition)