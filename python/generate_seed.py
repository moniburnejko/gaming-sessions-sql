"""
purpose:
- generate synthetic sql insert statements for the gaming sessions sql project.
- creates random but logically consistent data for postgresql.

how to run:
pip install faker
python generate_seed.py

output:
seed_data.sql
it can be loaded with:
psql -d gaming_db -f seed_data.sql
"""

from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP


# initialize configuration and helper
fake = Faker()
random.seed(42)

NUM_PLAYERS = 80
NUM_SESSIONS = 240
NUM_PURCHASES = 120

# helper date formatting functions
def fmt_ts(dt):  # format TIMESTAMP
    """Return datetime as 'YYYY-MM-DD HH:MM:SS'"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def fmt_d(d):  # format DATE
    """Return date as 'YYYY-MM-DD'"""
    return d.strftime('%Y-%m-%d')


def sql_escape(s: str) -> str:
    """escape single quotes for sql safety."""
    return s.replace("'", "''")


# generate players (with unique nicknames)
players = []
seen = set()
for i in range(1, NUM_PLAYERS + 1):
    while True:
        nickname = fake.user_name()
        if nickname not in seen:
            seen.add(nickname)
            break
    country = random.choice(['PL','DE','FR','GB','SE','US','ES','NL','IT'])
    signup_date = fake.date_between(start_date='-120d', end_date='-30d')
    players.append((i, nickname, country, signup_date))


# generate sessions
sessions = []
for i in range(1, NUM_SESSIONS + 1):
    pid = random.randint(1, NUM_PLAYERS)
    start = fake.date_time_between(start_date='-60d', end_date='now')
    end = start + timedelta(minutes=random.randint(15, 90))
    device = random.choice(['ps', 'xbox', 'pc', 'mobile'])
    sessions.append((i, pid, start, end, device))


# generate matches (1–5 per session; weighted results)
MODE_WEIGHTS = {'solo': 40, 'duos': 30,'squads': 10,'zero_build': 20}
RESULT_WEIGHTS = {'win': 10,'top10': 35,'loss': 55}

def weighted_pick(d: dict) -> str:
    keys = list(d.keys())
    weights = list(d.values())
    return random.choices(keys, weights=weights, k=1)[0]

matches = []
match_id = 1
for s in sessions:
    session_id = s[0]
    num_matches = random.randint(1, 5)

    for _ in range(num_matches):
        mode = weighted_pick(MODE_WEIGHTS)
        result = weighted_pick(RESULT_WEIGHTS)
        score = random.randint(50, 500)
        matches.append((match_id, session_id, mode, result, score))
        match_id += 1


# generate purchases
def money(value):
    """round to 2 decimals."""
    return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

PRICE_OPTIONS = {
    'Battle Pass': [12.99],
    'In-game Currency': [4.99, 9.99, 12.99, 21.99, 39.99],
    'Quest Pack': [2.99, 4.99, 16.99],
    'Emote': [1.99, 2.99, 3.99],
    'Legendary Skin': [16.99, 21.99, 29.99],
}

# weighted popularity of items (how often they appear)
ITEMS = list(PRICE_OPTIONS.keys())
WEIGHTS = [20, 50, 10, 5, 5]  # In-game Currency most frequent

purchases = []
for i in range(1, NUM_PURCHASES + 1):
    pid = random.randint(1, NUM_PLAYERS)
    # choose item based on popularity weights
    item = random.choices(ITEMS, weights=WEIGHTS, k=1)[0]
    # pick random price from list of possible prices for that item
    price_choice = random.choice(PRICE_OPTIONS[item])
    final_price = money(price_choice)
    purchased_at = fake.date_time_between(start_date='-45d', end_date='now')
    purchases.append((i, pid, item, final_price, purchased_at))


# write sql to file
with open("seed_data.sql", "w", encoding="utf-8") as f:
    f.write("-- Auto-generated synthetic data for Gaming Sessions SQL project\n")
    f.write("TRUNCATE purchases, matches, sessions, players RESTART IDENTITY CASCADE;\n\n")

    # players
    f.write("-- players\n")
    f.write("INSERT INTO players (player_id, nickname, country_code, signup_date) VALUES\n")
    f.write(",\n".join(
        [f"({p[0]},'{sql_escape(p[1])}','{p[2]}','{fmt_d(p[3])}')" for p in players]
    ))
    f.write(";\n\n")

    # sessions
    f.write("-- sessions\n")
    f.write("INSERT INTO sessions (session_id, player_id, started_at, ended_at, device) VALUES\n")
    f.write(",\n".join(
        [f"({s[0]},{s[1]},'{fmt_ts(s[2])}','{fmt_ts(s[3])}','{s[4]}')" for s in sessions]
    ))
    f.write(";\n\n")

    # matches
    f.write("-- matches\n")
    f.write("INSERT INTO matches (match_id, session_id, mode, result, score) VALUES\n")
    f.write(",\n".join(
        [f"({m[0]},{m[1]},'{m[2]}','{m[3]}',{m[4]})" for m in matches]
    ))
    f.write(";\n\n")

    # purchases
    f.write("-- purchases\n")
    f.write("INSERT INTO purchases (purchase_id, player_id, item_name, amount_usd, purchased_at) VALUES\n")
    f.write(",\n".join(
        [f"({p[0]},{p[1]},'{sql_escape(p[2])}',{str(p[3])},'{fmt_ts(p[4])}')" for p in purchases]
    ))
    f.write(";\n\n")

    # reset sequences to match max IDs
    f.write("-- reset sequences\n")
    f.write("""
SELECT setval('players_player_id_seq', (SELECT MAX(player_id) FROM players));
SELECT setval('sessions_session_id_seq', (SELECT MAX(session_id) FROM sessions));
SELECT setval('matches_match_id_seq', (SELECT MAX(match_id) FROM matches));
SELECT setval('purchases_purchase_id_seq', (SELECT MAX(purchase_id) FROM purchases));
""")

print("seed_data.sql generated successfully.")