import streamlit as st

import src.etl.bigquery.standings_to_bigquery as standings
import src.constants.constants as constants
from dotenv import load_dotenv

def app():
  load_dotenv(dotenv_path=constants.DOTENV_PATH)
  standings.start_pipeline()

if __name__=="__main__":
  app()