-- Report: retention_analysis
-- Purpose: analyze 7-day retention overall and by country.

-- Overall 7-day retention (percentage)
-- Single KPI from the dedicated view.
SELECT * FROM v_retention_7d;


-- Retention by country
-- Shows 7day retention per country_code.
SELECT p.country_code,
       ROUND(100.0 * COUNT(*) FILTER (WHERE r.return_day <= f.first_day + INTERVAL '7 days')
             / NULLIF(COUNT(*),0), 2) AS retention_7d_percent,
       COUNT(*) AS total_players
FROM v_first_play f
LEFT JOIN v_returns r USING(player_id)
JOIN players p USING(player_id)
GROUP BY p.country_code
ORDER BY retention_7d_percent DESC;