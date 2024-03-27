import streamlit as st

from src.etl.bigquery.standings import get_standings
from src.utils.constants import constants
from dotenv import load_dotenv

def app():
  load_dotenv(dotenv_path=constants.DOTENV_PATH)
  # Get standings from bigquery
  df = get_standings()
  # Display the standings as a table
  st.dataframe(
    data=df,
    hide_index=True
  )

if __name__=="__main__":
  app()