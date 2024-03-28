import streamlit as st

from src.etl.bigquery.standings import get_standings
from src.etl.bigquery.top_scorers import get_top_scorers
from src.utils.constants import constants
from dotenv import load_dotenv

def display_standings():
  st.markdown("Current Standings")
  # Get standings from bigquery
  standings = get_standings()
  # Display the standings as a table
  st.dataframe(
    data=standings,
    column_config= {
      "rank": "Rank",
      "crest": st.column_config.ImageColumn("Icon", width="small"),
      "team": "Team",
      "games_played": "Games Played",
      "wins": "Wins",
      "losses": "Losses",
      "draws": "Draws",
      "points": "Points",
      "goal_difference": "Goal Difference",
      "goals_for": "Goals For",
      "goals_against": "Goals Against"
    },
    hide_index=True,
    use_container_width=True
  )

def display_top_scorers():
  st.markdown("Top Scorers")
  # Get top scorers from bigquery
  top_scorers = get_top_scorers()
  # Display the top scorers as a table
  st.dataframe(
    data=top_scorers,
    column_config={
      "name": "Player",
      "team": "Team",
      "goals": "Goals",
      "assists": "Assists",
      "matches_played": "Matches Played",
      "nationality": "Nationality"
    },
    use_container_width=True,
    hide_index=True
  )

def app():
  st.set_page_config(
    page_title="Football Live",
    layout="wide",
    initial_sidebar_state="auto",
  )
  load_dotenv(dotenv_path=constants.DOTENV_PATH)
  # Display header
  st.header("Football Live")

  # Create tabs
  tab1, tab2, tab3 = st.tabs(["Standings", "Top Scorers", "Matchday"])

  with tab1:
    # Display current standings
    display_standings()

  with tab2:
    # Display current top scorers
    display_top_scorers()
  with tab3:
    pass

  

if __name__=="__main__":
  app()