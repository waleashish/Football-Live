import pandas as pd
from pandas import DataFrame
from src.utils.DBConnection import DBConnection

def get_top_scorers(league_id: int) -> DataFrame:
    conn = DBConnection().get_connection()
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

def get_fixtures(league_id: int) -> DataFrame:
    conn = DBConnection().get_connection()
    cur = conn.cursor()
    exec_query = f"""
        SELECT
            t1.crest AS home_crest,
            t1.short_name AS home_team,
            f.home_team_score AS home_score,
            t2.crest AS away_crest,
            t2.short_name AS away_team,
            f.away_team_score AS away_score,
            f.status,
            f.matchday
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.team_id
        JOIN teams t2 ON f.away_team_id = t2.team_id
        WHERE f.league_id = {league_id}
        ORDER BY f.matchday DESC
    """

    cur.execute(exec_query)
    fixtures = cur.fetchall()

    df = DataFrame(
        fixtures,
        columns=[
            "home_crest",
            "home_team",
            "home_score",
            "away_crest",
            "away_team",
            "away_score",
            "status",
            "matchday"
        ]
    )

    df['home_score'] = df['home_score'].apply(lambda x: x if pd.notnull(x) else "-")
    df['away_score'] = df['away_score'].apply(lambda x: x if pd.notnull(x) else "-")

    df["home_score"] = df["home_score"].apply(lambda x: int(x) if x != "-" else x)
    df["away_score"] = df["away_score"].apply(lambda x: int(x) if x != "-" else x)


    return df