import streamlit as st

import src.etl.bigquery.standings_to_bigquery as standings
from src.etl.bigquery.standings import get_standings
import src.constants.constants as constants
from dotenv import load_dotenv

def app():
  load_dotenv(dotenv_path=constants.DOTENV_PATH)
  # Load data into bigquery.
  standings.start_pipeline()
  # Get standings from bigquery
  df = get_standings()
  # Display the standings as a table
  st.dataframe(
    data=df
  )

if __name__=="__main__":
  app()