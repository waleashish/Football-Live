CREATE TABLE leagues (
    league_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    team_count INT NOT NULL
);

CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    crest VARCHAR(255) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    league_id INTEGER REFERENCES leagues(league_id)
);

CREATE TABLE top_scorers (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    team_id INTEGER REFERENCES teams(team_id),
    goals INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    league_id INTEGER REFERENCES leagues(league_id)
);


CREATE TABLE standings (
    team_id INTEGER REFERENCES teams(team_id),
    league_id INTEGER REFERENCES leagues(league_id),
    position INTEGER NOT NULL,
    points INTEGER NOT NULL,
    matches_played INTEGER NOT NULL,
    wins INTEGER NOT NULL,
    draws INTEGER NOT NULL,
    losses INTEGER NOT NULL,
    goals_for INTEGER NOT NULL,
    goals_against INTEGER NOT NULL,
    goal_difference INTEGER NOT NULL
);


CREATE TABLE fixtures (
    fixture_id INT PRIMARY KEY,
    home_team_id INTEGER REFERENCES teams(team_id),
    away_team_id INTEGER REFERENCES teams(team_id),
    league_id INTEGER REFERENCES leagues(league_id),
    status VARCHAR(255) NOT NULL,
    home_team_score INTEGER,
    away_team_score INTEGER,
    matchday INTEGER NOT NULL
);