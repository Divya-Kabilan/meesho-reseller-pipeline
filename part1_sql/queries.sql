-- 1. Monthly revenue by category
SELECT 
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY 
    CASE month 
        WHEN 'April' THEN 1 
        WHEN 'May' THEN 2 
        WHEN 'June' THEN 3 
    END,
    category;

-- 2. Region-wise total revenue and order count
SELECT 
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(o.order_id) AS total_orders
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

-- 3. Top resellers by total spend (> 50,000)
SELECT 
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- 4. Zero-order reseller identification & COUNT(*) vs COUNT(order_id) demo
SELECT 
    r.reseller_id,
    r.reseller_name,
    r.region,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name, r.region
HAVING COUNT(o.order_id) = 0;

-- 5. Average Order Value (AOV) for June, Delivered orders only
SELECT 
    ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June' AND status = 'Delivered';