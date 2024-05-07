import psycopg2
import time
from pandas import DataFrame

from src.utils.DBConnection import DBConnection

def get_top_scorers(league_id: int) -> DataFrame:
    while True:
        try:
            conn = psycopg2.connect(
                dbname="football",
                user="football",
                password="football",
                host="postgres-football"
            )
            break

        except psycopg2.OperationalError:
            time.sleep(1)

    cur = conn.cursor()
    exec_query = f"""
        SELECT
            t.crest,
            ts.player_name,
            ts.goals,
            ts.assists
        FROM top_scorers ts JOIN teams t ON ts.team_id = t.team_id
        WHERE ts.league_id = {league_id}
        ORDER BY ts.goals DESC
    """
    cur.execute(exec_query)
    top_scorers = cur.fetchall()

    # Create a DataFrame from the data and return it but ommit the league_id column
    df = DataFrame(
        top_scorers,
        columns=["crest", "name", "goals", "assists"]
    )

    return df

def get_standings(league_id: int) -> DataFrame:
    # Get a connection to the database
    conn = DBConnection().get_connection()
    cur = conn.cursor()
    exec_query = f"""
        SELECT
            s.position,
            t.crest,
            t.name AS team,
            s.matches_played AS matches,
            s.wins,
            s.losses,
            s.draws,
            s.goals_for,
            s.goals_against,
            s.goal_difference,
            s.points
        FROM standings s JOIN teams t ON s.team_id = t.team_id
        WHERE s.league_id = {league_id}
        ORDER BY s.position ASC
    """

    cur.execute(exec_query)
    standings = cur.fetchall()

    # Create a DataFrame from the data and return it
    df = DataFrame(
        standings,
        columns=[
            "position",
            "crest",
            "team",
            "matches",
            "wins",
            "losses",
            "draws",
            "goals_for",
            "goals_against",
            "goal_difference",
            "points"
        ]
    )

    return df