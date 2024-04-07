from . import league_name_constants

DOTENV_PATH="config/.env"
CREDENTIALS_PATH="config/credentials.json"

GCLOUD_PROJECT = "GCLOUD_PROJECT"

FOOTBALL_API = "api.football-data.org"
FOOTBALL_API_KEY = "FOOTBALL_API_KEY"
FOOTBALL = "Football"

TEAM_DROPDOWN_LIST = {
    "Select": None, 
    "Premier League": league_name_constants.PREMIER_LEAGUE,
    "La Liga": league_name_constants.LA_LIGA,
    "Serie A": league_name_constants.SERIE_A,
    "Bundesliga": league_name_constants.BUNDESLIGA,
    "Ligue 1": league_name_constants.LIGUE_1
}