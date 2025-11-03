## 🎮 gaming sessions sql analysis 
analysis of **player behavior**, **engagement**, **monetization**, and **retention** in a simulated online game environment.  
the project demonstrates a complete analytics workflow - from data generation with [**Faker**](https://github.com/joke2k/faker),  
through data modeling and sql views in **PostgreSQL**, to visualization and kpi reporting with **python (Matplotlib + Pandas)**.

### quick start
```bash
# clone the repository
git clone https://github.com/moniburnejko/gaming-sessions-sql.git
cd gaming-sessions-sql

# create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r python/requirements.txt

# set environment (optional for charts)
cp .env.example .env  # then edit values

# create postgres database
psql -U postgres
CREATE DATABASE gaming_db;
\c gaming_db

# load schema and seed data
psql -d gaming_db -f sql/schema/create_tables.sql
psql -d gaming_db -f sql/data/seed_data.sql

# or generate fresh synthetic data
python python/generate_seed.py
psql -d gaming_db -f seed_data.sql

# add analytical views
psql -d gaming_db -f sql/views/v_daily_kpis.sql
psql -d gaming_db -f sql/views/v_top_spenders.sql
psql -d gaming_db -f sql/views/v_wau_mau_ratio.sql
psql -d gaming_db -f sql/views/v_retention_7d.sql

# build charts and export csvs
python python/make_charts.py
```
the project will populate PostgreSQL with synthetic gameplay + purchases, create views, and export csvs and charts under `out/`.

## example outputs and behavior
### primary outputs:
- **csv exports** in `out/csv/` (e.g., daily kpis, monetization, retention)
- **charts** in `out/img/`:
  - `trend_dau.png`
  - `trend_revenue.png`
  - `win_rate_by_mode.png`
  - `avg_session_time_by_device.png`
  - `retention7d_by_country.png`
  - `returned_pie.png`
    
### behavior summary:
- **data generation** (`python/generate_seed.py`)
  - players: unique nicknames, country codes, signup dates  
  - sessions: 15–90 min duration; device in {'pc','xbox','ps','mobile'}  
  - matches: 1–5 per session; weighted modes/results for realism  
  - purchases: weighted item popularity; prices rounded to cents  
- **schema constraints** (`sql/create_tables.sql`)
  - foreign keys with cascade deletes; device/mode/result checks; nonnegative amounts/scores; session time validity  
- **views**
  - **v_daily_kpis** - aggregates daily core metrics: active users (DAU), session count, matches played, total revenue, and distinct payers.  
  - **v_top_spenders** - ranks players by total in-game spending; includes purchase count, total amount spent, average purchase value, and last purchase date.  
  - **v_wau_mau_ratio** - computes weekly and monthly active users (WAU, MAU) using rolling windows, and calculates the DAU/MAU ratio to measure engagement consistency.  
  - **v_retention_7d** - measures 7-day retention: the percentage of players who return within seven days after their first recorded session.  
- **reports** (`sql/reports/`)
  - `gameplay_metrics.sql`  
  - `monetization_metrics.sql`  
  - `retention_metrics.sql`


### architecture and modules
- **sql schema**
  - tables: `players`, `sessions`, `matches`, `purchases`
  - integrity: primary/foreign keys, check constraints, cascades
- **analytical views**
  - `v_daily_kpis`, `v_top_spenders`, `v_wau_mau_ratio`, `v_retention_7d`
- **python**
  - `generate_seed.py`
    - helpers: `fmt_ts`, `fmt_d`, `sql_escape`, `weighted_pick`
    - tunables: `NUM_PLAYERS`, `NUM_SESSIONS`, `NUM_PURCHASES`, item price menus
  - `make_charts.py`
    - connects via [**psycopg2**](https://github.com/psycopg/psycopg2), queries views, saves CSVs and Matplotlib charts

### configuration reference
the charts/export step reads environment variables (via **dotenv**) for db access and output paths.

| variable | description | default |
|-----------|--------------|----------|
| **DB_HOST** | PostgreSQL host | `localhost` |
| **DB_PORT** | PostgreSQL port | `5432` |
| **DB_NAME** | database name | `gaming_db` |
| **DB_USER** | database user | `postgres` |
| **DB_PASSWORD** | database password | *(none)* |
| **OUTPUT_DIR** | base output directory for CSVs and charts | `./out` |

**example `.env`:**
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gaming_db
DB_USER=postgres
DB_PASSWORD=your_password
OUTPUT_DIR=out
```

### examples
- **sql reports** (`sql/reports/`)
  - `gameplay_metrics.sql` - session duration, win rate, activity ratios, and key performance metrics.
  - `monetization_metrics.sql` - top spenders, ARPPU (average revenue per paying user), and relationship between engagement and purchases.
  - `retention_metrics.sql` - 7-day retention overall and by country.
- **outputs** generated in `out/csv/` and `out/img/` after running `make_charts.py`.

### contributing
prs and issues welcome! if you change the schema or views, please update the README and example reports.

#### license
this project is released under the mit license.  

### let's connect!   
[![linkedin](https://img.shields.io/badge/linkedin-000000?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/monika-burnejko-9301a1357/) [![kaggle](https://img.shields.io/badge/kaggle-000000?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/monikaburnejko) [![portfolio](https://img.shields.io/badge/portfolio-000000?style=for-the-badge&logo=notion&logoColor=white)](https://www.notion.so/monikaburnejko/Data-Analytics-Portfolio-2761bac67ca9807298aee038976f0085) [![email](https://img.shields.io/badge/email-000000?style=for-the-badge&logo=gmail&logoColor=white)](mailto:moniaburnejko@gmail.com)
