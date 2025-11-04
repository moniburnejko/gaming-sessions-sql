"""
make_charts.py
purpose: pull key sql reports from the Gaming Sessions DB and produce CSVs and charts.
"""

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# charts style
COLORS = {"line": "#44546A", "bar": "#419FB5", "pie": ["#44546A", "#419FB5"]}

plt.rcParams.update({
    "axes.facecolor": "white",
    "axes.edgecolor": "#E0E0E0",
    "axes.grid": False,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
})

# env & config
load_dotenv()
PGHOST = os.getenv("PGHOST")
PGPORT = int(os.getenv("PGPORT"))
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")

#outputs paths
OUT_CSV = Path("out/csv"); OUT_IMG = Path("out/img")
OUT_CSV.mkdir(parents=True, exist_ok=True); OUT_IMG.mkdir(parents=True, exist_ok=True)

def query_df(sql: str, params=None) -> pd.DataFrame:
    """run SQL and return results as a pandas DataFrame."""
    with psycopg2.connect(host=PGHOST, port=PGPORT, dbname=PGDATABASE, user=PGUSER, password=PGPASSWORD) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return pd.DataFrame(cur.fetchall())

def save_csv(df: pd.DataFrame, name: str) -> Path:
    """write dataframe to CSV in the standard output folder."""
    path = OUT_CSV / name; df.to_csv(path, index=False); return path

def line_chart(df, x, y, title, out_name, ylabel=""):
    """render time-series line chart and save it to out/img."""
    df = df.copy()
    df[x] = pd.to_datetime(df[x])
    df = df.sort_values(x)

    plt.figure(figsize=(8, 4))
    plt.plot(df[x], df[y], color=COLORS["line"])

    ax = plt.gca()
    locator = mdates.DayLocator(interval=5)
    formatter = mdates.DateFormatter('%b %d')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_xlabel('')
    if ylabel:
        ax.set_ylabel(ylabel)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(OUT_IMG / out_name)
    plt.close()


def bar_chart(df, x, y, title, out_name, xlabel="", ylabel=""):
    """render categorical bar chart and save it to out/img."""
    plt.figure(figsize=(7, 4))
    plt.bar(df[x], df[y], color=COLORS["bar"])
    plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(OUT_IMG / out_name)
    plt.close()


def pie_chart(labels, sizes, title, out_name):
    """render pie chart with percentage labels and save it to out/img."""
    plt.figure(figsize=(5, 5))
    plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=COLORS["pie"],
        startangle=90
    )
    plt.title(title)
    plt.tight_layout()
    plt.savefig(OUT_IMG / out_name)
    plt.close()


"""predefined SQL queries used for key reports:
- daily KPIs
- win rate by mode
- session time by device
- ARPDAU trend
- retention by country
- return status pie
 """
SQL_TREND = """
SELECT day, dau, sessions, revenue_usd
FROM v_daily_kpis
ORDER BY day;
"""
SQL_WINRATE = """
SELECT mode,
       ROUND(100.0 * COUNT(*) FILTER (WHERE result = 'win') / COUNT(*), 2) AS win_rate_pct,
       COUNT(*) AS matches
FROM matches
GROUP BY mode
ORDER BY win_rate_pct DESC, mode;
"""
SQL_SESSION_TIME = """
SELECT device,
       ROUND(AVG(EXTRACT(EPOCH FROM (ended_at - started_at)) / 60), 2) AS avg_min
FROM sessions
GROUP BY device
ORDER BY avg_min DESC, device;
"""
SQL_ARPDAU_14 = """
SELECT day, dau, revenue_usd, ROUND(CASE WHEN dau > 0 THEN revenue_usd / dau ELSE 0 END, 2) AS arp_dau
FROM v_daily_kpis
ORDER BY day DESC
LIMIT 14;
"""
SQL_RETENTION_COUNTRY = """
SELECT p.country_code,
       ROUND(100.0 * COUNT(*) FILTER (WHERE r.return_day <= f.first_day + INTERVAL '7 days')
             / NULLIF(COUNT(*), 0), 2) AS retention_7d_percent,
       COUNT(*) AS total_players
FROM v_first_play f
LEFT JOIN v_returns r USING (player_id)
JOIN players p USING (player_id)
GROUP BY p.country_code
ORDER BY retention_7d_percent DESC, p.country_code;
"""
SQL_RETURNED_PIE = """
SELECT CASE WHEN r.return_day IS NOT NULL THEN 'Returned' ELSE 'Did not return' END AS group_type,
       COUNT(*) AS players
FROM v_first_play f
LEFT JOIN v_returns r USING(player_id)
GROUP BY group_type
ORDER BY group_type;
"""

def main():
    """run all report queries, save results as CSVs, and generate charts."""
    df_trend = query_df(SQL_TREND)
    if not df_trend.empty:
        save_csv(df_trend, "trend_daily_kpis.csv")
        line_chart(df_trend, "day", "dau", "DAU over time", "trend_dau.png", ylabel="DAU")
        line_chart(df_trend, "day", "revenue_usd", "Revenue over time", "trend_revenue.png", ylabel="USD")

    df_win = query_df(SQL_WINRATE)
    if not df_win.empty:
        save_csv(df_win, "win_rate_by_mode.csv")
        bar_chart(df_win, "mode", "win_rate_pct", "Win rate by mode (%)", "win_rate_by_mode.png", xlabel="mode", ylabel="%")

    df_sess = query_df(SQL_SESSION_TIME)
    if not df_sess.empty:
        save_csv(df_sess, "avg_session_time_by_device.csv")
        bar_chart(df_sess, "device", "avg_min", "Average session time per device (min)", "avg_session_time_by_device.png",
                  xlabel="device", ylabel="minutes")

    df_arpdau = query_df(SQL_ARPDAU_14)
    if not df_arpdau.empty:
        save_csv(df_arpdau, "arpdau_last_14_days.csv")
        line_chart(df_arpdau.sort_values("day"), "day", "arp_dau", "ARPDAU - last 14 days", "arpdau_last_14_days.png", ylabel="USD per DAU")

    df_ret_country = query_df(SQL_RETENTION_COUNTRY)
    if not df_ret_country.empty:
        save_csv(df_ret_country, "retention7d_by_country.csv")
        bar_chart(df_ret_country, "country_code", "retention_7d_percent", "7-day retention by country (%)", "retention7d_by_country.png",
                  xlabel="country", ylabel="%")

    df_ret_pie = query_df(SQL_RETURNED_PIE)
    if not df_ret_pie.empty:
        save_csv(df_ret_pie, "returned_vs_not.csv")
        labels = df_ret_pie["group_type"].tolist()
        sizes = df_ret_pie["players"].tolist()
        pie_chart(labels, sizes, "Returned within 7 days", "returned_pie.png")

    print("Done. Check folders: out/csv and out/img")

if __name__ == "__main__":
    main()
