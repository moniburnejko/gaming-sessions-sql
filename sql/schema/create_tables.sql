-- create_tables.sql
-- Purpose: defines the database schema for the Gaming Sessions SQL project. 
-- Includes all core entities (players, sessions, matches, purchases) 
-- with primary and foreign key relationships.

CREATE TABLE players (
  player_id SERIAL PRIMARY KEY,
  nickname TEXT NOT NULL UNIQUE,
  country_code CHAR(2) NOT NULL,
  signup_date DATE NOT NULL
);

CREATE TABLE sessions (
  session_id SERIAL PRIMARY KEY,
  player_id INT NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
  started_at TIMESTAMP NOT NULL,
  ended_at TIMESTAMP NOT NULL,
  device TEXT NOT NULL CHECK (device IN ('pc','xbox','ps','mobile')),
  CONSTRAINT session_time_ok CHECK (ended_at >= started_at)
);

CREATE TABLE matches (
  match_id SERIAL PRIMARY KEY,
  session_id INT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
  mode TEXT NOT NULL CHECK (mode IN ('solo','duos','squads','zero_build')),
  result TEXT NOT NULL CHECK (result IN ('win','top10','loss')),
  score INT NOT NULL CHECK (score >= 0)
);

CREATE TABLE purchases (
  purchase_id SERIAL PRIMARY KEY,
  player_id INT NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
  item_name TEXT NOT NULL,
  amount_usd NUMERIC(8,2) NOT NULL CHECK (amount_usd >= 0),
  purchased_at TIMESTAMP NOT NULL
);