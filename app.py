import streamlit as st

from src.etl.bigquery.standings import get_standings
from src.etl.bigquery.top_scorers import get_top_scorers
from src.etl.bigquery import transfer_top_scorers, transfer_standings
from src.utils.constants import constants
from dotenv import load_dotenv

def app():
  load_dotenv(dotenv_path=constants.DOTENV_PATH)
  # Display header
  st.header("Football Live ...")
  
  # Get standings from bigquery
  standings = get_standings()
  # Display the standings as a table
  st.dataframe(
    data=standings,
    hide_index=True
  )

  # Get top scorers from bigquery
  top_scorers = get_top_scorers()
  # Display the top scorers as a table
  st.dataframe(
    data=top_scorers,
    hide_index=True
  )

if __name__=="__main__":
  app()