-- View: v_top_spenders
-- Purpose: ranks players by total in-game spending. 
-- Aggregates purchase count, total and average spend, and last purchase date per player.
-- Used to identify high-value users and analyze monetization behavior.

CREATE OR REPLACE VIEW v_top_spenders AS
SELECT
    p.player_id,
    p.nickname,
    COUNT(*) AS purchases_cnt,
    SUM(pr.amount_usd)::numeric(10,2) AS total_spent,
    ROUND(AVG(pr.amount_usd), 2) AS avg_purchase_value,
    MAX(pr.purchased_at) AS last_purchase
FROM purchases pr
JOIN players p ON p.player_id = pr.player_id
GROUP BY p.player_id, p.nickname
ORDER BY total_spent DESC;