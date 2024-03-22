import os

from .connector import Connector
import src.constants.constants as constants
import requests

class Football:
  def __init__(self) -> None:
    connector = Connector(constants.FOOTBALL)
    self.conn = connector.connect()

  def fetch_pl_matches(self):
    payload = ''
    GET_PL_MATCHES_URL = "/v4/competitions/PL/matches"
    headers = {
      'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
    }
    self.conn.request("GET", GET_PL_MATCHES_URL, payload, headers)
    res = self.conn.getresponse()
    return res.read().decode("utf-8")
  
  def fetch_pl_standings(self):
    url = "http://api.football-data.org/v4/competitions/PL/standings"

    payload = {}
    headers = {
      'X-Auth-Token': os.getenv(constants.FOOTBALL_API_KEY)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # payload = ''
    # headers = {
    #   'X-Auth-Token': os.getenv(connection_constants.FOOTBALL_API_KEY)
    # }
    # self.conn.request("GET", "/v4/competitions/PL/standings", payload, headers)
    # res = self.conn.getresponse()
    return response.json()