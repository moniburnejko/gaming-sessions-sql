-- View: v_wau
-- Purpose: calculates Weekly Active Users (WAU) using a 7-day rolling window over player activity. 
-- Useful for tracking medium-term engagement and retention.

CREATE OR REPLACE VIEW v_wau AS
WITH bounds AS (
  SELECT MIN(DATE(started_at)) AS d0, MAX(DATE(started_at)) AS d1 FROM sessions),
days AS (
  SELECT GENERATE_SERIES(d0, d1, INTERVAL '1 day')::date AS day FROM bounds)
SELECT d.day,
       COUNT(DISTINCT s.player_id) AS wau
FROM days d
LEFT JOIN sessions s
  ON DATE(s.started_at) BETWEEN d.day - INTERVAL '6 day' AND d.day
GROUP BY d.day
ORDER BY d.day;


-- View: v_mau
-- Purpose: calculates Monthly Active Users (MAU) using a 30-day rolling window.
-- Used to assess long-term engagement and player base stability.

CREATE OR REPLACE VIEW v_mau AS
WITH bounds AS (
  SELECT MIN(DATE(started_at)) AS d0, MAX(DATE(started_at)) AS d1 FROM sessions),
days AS (
  SELECT GENERATE_SERIES(d0, d1, INTERVAL '1 day')::date AS day FROM bounds)
SELECT d.day,
       COUNT(DISTINCT s.player_id) AS mau
FROM days d
LEFT JOIN sessions s
  ON DATE(s.started_at) BETWEEN d.day - INTERVAL '29 day' AND d.day
GROUP BY d.day
ORDER BY d.day;


-- View: v_dau_mau_ratio
-- Purpose: joins DAU and MAU metrics to calculate the DAU/MAU ratio per day. 
-- Indicates stickiness - how often monthly active users return daily.

CREATE OR REPLACE VIEW v_dau_mau_ratio AS
SELECT d.day,
       d.dau,
       m.mau,
       CASE WHEN m.mau > 0 THEN ROUND(d.dau::numeric / m.mau, 4) ELSE 0 END AS dau_mau_ratio
FROM v_daily_kpis d
LEFT JOIN v_mau m USING(day)
ORDER BY d.day;