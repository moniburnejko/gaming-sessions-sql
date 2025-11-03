-- View: v_daily_kpis
-- Purpose: aggregates daily performance metrics including DAU, sessions, matches, revenue, and payers.
-- Used to monitor key product KPIs such as player activity and monetization trends over time.

CREATE OR REPLACE VIEW v_daily_kpis AS
WITH dau AS (
  SELECT DATE(started_at) AS d, COUNT(DISTINCT player_id) AS dau
  FROM sessions GROUP BY 1),
  
sess AS (
  SELECT DATE(started_at) AS d, COUNT(*) AS sessions_cnt
  FROM sessions GROUP BY 1),
  
mtch AS (
  SELECT DATE(s.started_at) AS d, COUNT(m.match_id) AS matches_cnt
  FROM matches m JOIN sessions s ON s.session_id = m.session_id
  GROUP BY 1),
  
rev AS (
  SELECT DATE(purchased_at) AS d, SUM(amount_usd) AS revenue, COUNT(DISTINCT player_id) AS payers
  FROM purchases GROUP BY 1)
  
SELECT d.d AS day,
       COALESCE(dau.dau,0) AS dau,
       COALESCE(sess.sessions_cnt,0) AS sessions,
       COALESCE(mtch.matches_cnt,0) AS matches,
       COALESCE(rev.revenue,0)::numeric(10,2) AS revenue_usd,
       COALESCE(rev.payers,0) AS payers
FROM (
  SELECT DATE(started_at) AS d FROM sessions
  UNION
  SELECT DATE(purchased_at) AS d FROM purchases) d
LEFT JOIN dau ON dau.d = d.d
LEFT JOIN sess ON sess.d = d.d
LEFT JOIN mtch ON mtch.d = d.d
LEFT JOIN rev ON rev.d = d.d
ORDER BY day;