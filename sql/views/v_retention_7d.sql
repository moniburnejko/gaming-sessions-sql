-- View: v_first_play  
-- Purpose: identifies the first day each player started playing.  
-- Used as the foundation for retention analysis.  

CREATE OR REPLACE VIEW v_first_play AS
SELECT 
    player_id,
    MIN(DATE(started_at)) AS first_day
FROM sessions
GROUP BY 1;CREATE OR REPLACE VIEW v_first_play AS
SELECT player_id, MIN(DATE(started_at)) AS first_day FROM sessions GROUP BY 1;


-- View: v_returns  
-- Purpose: captures the first return day for each player after their initial session.  
-- Joined with v_first_play to calculate player retention metrics (e.g., 7-day retention).  

CREATE OR REPLACE VIEW v_returns AS
SELECT 
    s.player_id,
    MIN(DATE(s.started_at)) AS return_day
FROM sessions s
JOIN v_first_play f USING (player_id)
WHERE DATE(s.started_at) > f.first_day
GROUP BY 1;CREATE OR REPLACE VIEW v_returns AS
SELECT s.player_id, MIN(DATE(s.started_at)) AS return_day
FROM sessions s JOIN v_first_play f USING(player_id)
WHERE DATE(s.started_at) > f.first_day GROUP BY 1;


-- View: v_retention_7d
-- Purpose: measures the 7-day retention rate - the percentage of players who return within 7 days 
-- after their first recorded session. 
-- Used to evaluate early engagement and onboarding effectiveness.

CREATE OR REPLACE VIEW v_retention_7d AS
SELECT 
  ROUND(
    100.0 * COUNT(*) FILTER (WHERE r.return_day <= f.first_day + INTERVAL '7 days')
    / NULLIF(COUNT(*),0), 
  2) AS retention_7d_percent
FROM v_first_play f
LEFT JOIN v_returns r USING(player_id);