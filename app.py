import streamlit as st

from src.ui.fixtures import handle_fixture_display
from src.utils.constants import constants
from src.load import get_data

def display_standings(competition):
  st.markdown("Current Standings")
  # Get standings from bigquery
  standings = get_data.get_standings(constants.league_ids[competition])
  # Display the standings as a table
  st.dataframe(
    data=standings,
    column_config= {
      "position": "Rank",
      "crest": st.column_config.ImageColumn("Icon", width="small"),
      "team": "Team",
      "matches": "Matches",
      "wins": "Wins",
      "losses": "Losses",
      "draws": "Draws",
      "goals_for": "Goals For",
      "goals_against": "Goals Against",
      "goal_difference": "Goal Difference",
      "points": "Points"
    },
    hide_index=True,
    use_container_width=True
  )

def display_top_scorers(competition):
  st.markdown("Top Scorers")
  # Get top scorers from bigquery
  top_scorers = get_data.get_top_scorers(constants.league_ids[competition])
  # Display the top scorers as a table
  st.dataframe(
    data=top_scorers,
    column_config={
      "crest": st.column_config.ImageColumn("Icon", width="small"),
      "name": "Name",
      "goals": "Goals",
      "assists": "Assists"
    },
    use_container_width=True,
    hide_index=True
  )

def display_fixtures(competition):
  handle_fixture_display(constants.league_ids[competition])

def app():
  st.set_page_config(
    page_title="Football Live",
    layout="wide",
    initial_sidebar_state="auto",
  )
  # Display header
  st.header("Football Live")

  # Create dropdown to select competition
  option = st.selectbox(
    'Competition',
    options=constants.TEAM_DROPDOWN_LIST.keys())
  
  render_app(option)
  
def render_app(option):
  # Create tabs
  tab1, tab2, tab3 = st.tabs(["Standings", "Top Scorers", "Fixtures"])
  if option != "Select":
    with tab1:
      # Display current standings
      display_standings(constants.TEAM_DROPDOWN_LIST[option])

    with tab2:
      # Display current top scorers
      display_top_scorers(constants.TEAM_DROPDOWN_LIST[option])
    with tab3:
      # Display the fixtures matchday-wise
      display_fixtures(constants.TEAM_DROPDOWN_LIST[option])

if __name__=="__main__":
  app()