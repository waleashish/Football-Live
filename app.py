import json

from dotenv import load_dotenv
from api.football import Football

def app():
  load_dotenv()
  football = Football()
  matches = football.fetch_pl_matches()
  d = json.loads(matches)
  print(type(d))
  print(matches)


if __name__=="__main__":
  app()