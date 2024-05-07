import psycopg2
import time
from pandas import DataFrame

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
