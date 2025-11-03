-- Report: gameplay_metrics
-- Purpose: analyze player engagement and gameplay behavior using daily KPIs and match data.
-- Includes session duration, win rate, activity ratios, and key performance metrics.

-- Average session time per device (in minutes)
-- Shows average gameplay duration across devices: pc, ps, xbox, mobile.
SELECT device,
       ROUND(AVG(EXTRACT(EPOCH FROM (ended_at-started_at))/60),2) avg_min
FROM sessions 
GROUP BY device 
ORDER BY avg_min DESC;

-- Win rate per mode
-- Calculates win percentage for each game mode (solo, duos, squads, zero_build).
SELECT mode,
       ROUND(100.0*COUNT(*) FILTER (WHERE result='win')/COUNT(*),2) win_rate_pct,
       COUNT(*) matches
FROM matches 
GROUP BY mode 
ORDER BY win_rate_pct DESC;

-- ARPDAU (Average Revenue Per Daily Active User)
-- Derived from v_daily_kpis: measures monetization efficiency per active user.
SELECT day, dau, revenue_usd, ROUND(CASE WHEN dau>0 THEN revenue_usd/dau ELSE 0 END,2) arp_dau
FROM v_daily_kpis 
ORDER BY day DESC 
LIMIT 14;

-- Stickiness (DAU/MAU ratio)
-- Identifies most engaging days based on user retention and activity.
SELECT day, dau, mau, dau_mau_ratio
FROM v_dau_mau_ratio
ORDER BY dau_mau_ratio DESC 
LIMIT 10;

-- Weekly vs Monthly Active Users
-- Compares WAU and MAU trends over the last 14 days.
SELECT w.day, w.wau, m.mau
FROM v_wau w 
JOIN v_mau m USING(day)
ORDER BY w.day DESC 
LIMIT 14;

-- Last 10 Days - Daily KPIs Overview
-- Displays key daily metrics: DAU, sessions, matches, revenue, payers.
SELECT * FROM v_daily_kpis 
ORDER BY day DESC 
LIMIT 10;