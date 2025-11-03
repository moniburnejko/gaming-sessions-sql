-- Report: monetization_metrics
-- Purpose: analyze player spending behavior, revenue distribution, and relationship between engagement and purchases.

-- Top 10 spenders
-- Identifies the highest-spending players by total purchase amount.
SELECT * FROM v_top_spenders 
LIMIT 10;

-- Active payers (last 30 days)
-- Finds players who made at least one purchase in the last 30 days.
SELECT * FROM v_top_spenders
WHERE last_purchase > NOW() - INTERVAL '30 days';

-- ARPPU (Average Revenue Per Paying User)
-- Calculates the average revenue among all players who have spent money.
SELECT ROUND(AVG(total_spent), 2) AS avg_revenue_per_payer
FROM v_top_spenders;

-- Spending vs activity
-- Checks whether high spenders are also more active (number of sessions).
SELECT t.nickname, t.total_spent, COUNT(s.session_id) AS sessions
FROM v_top_spenders t
JOIN sessions s ON s.player_id = t.player_id
GROUP BY t.nickname, t.total_spent
ORDER BY t.total_spent DESC;

-- Do returning players spend more?
-- Compares spending behavior between returning and non-returning players.
SELECT 
  CASE WHEN r.return_day IS NOT NULL THEN 'Returned' ELSE 'Did not return' END AS group_type,
  COUNT(*) AS players,
  SUM(p.amount_usd) AS total_spent,
  ROUND(AVG(p.amount_usd), 2) AS avg_spent
FROM v_first_play f
LEFT JOIN v_returns r USING(player_id)
LEFT JOIN purchases p USING(player_id)
GROUP BY group_type
ORDER BY total_spent DESC;