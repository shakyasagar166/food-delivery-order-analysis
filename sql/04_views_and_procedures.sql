-- ============================================================================
-- Project: Food Delivery Order Analysis
-- File: 04_views_and_procedures.sql
-- Description: Business Intelligence Views and Operational Stored Procedures.
-- ============================================================================

USE food_delivery_db;

-- ----------------------------------------------------------------------------
-- 1. View: v_daily_sales_summary
-- Purpose: Pre-aggregated daily trend view ready for Power BI / Tableau connection.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_daily_sales_summary AS
SELECT 
    o.order_date,
    c.city,
    COUNT(o.order_id) AS total_orders_placed,
    SUM(CASE WHEN o.order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(SUM(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE 0 END), 2) AS net_gmv,
    ROUND(SUM(CASE WHEN o.order_status = 'Delivered' THEN o.discount_amount ELSE 0 END), 2) AS total_discount,
    ROUND(AVG(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE NULL END), 2) AS aov
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY o.order_date, c.city;


-- ----------------------------------------------------------------------------
-- 2. View: v_restaurant_performance_matrix
-- Purpose: Evaluates restaurant quality, commercial volume, and commission yield.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_restaurant_performance_matrix AS
SELECT 
    r.restaurant_id,
    r.restaurant_name,
    r.city,
    r.cuisine_type,
    r.rating AS restaurant_rating,
    r.commission_rate,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    ROUND(SUM(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE 0 END), 2) AS total_sales,
    ROUND(SUM(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount * r.commission_rate ELSE 0 END), 2) AS platform_revenue,
    ROUND(AVG(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE NULL END), 2) AS avg_order_value
FROM restaurants r
LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, r.restaurant_name, r.city, r.cuisine_type, r.rating, r.commission_rate;


-- ----------------------------------------------------------------------------
-- 3. View: v_delivery_sla_audit
-- Purpose: Telemetry view for fleet monitoring and delivery bottlenecks.
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_delivery_sla_audit AS
SELECT 
    d.delivery_id,
    d.order_id,
    o.order_date,
    c.city,
    d.rider_id,
    rd.rider_name,
    rd.vehicle_type,
    d.distance_km,
    d.estimated_delivery_mins,
    d.actual_delivery_mins,
    (d.actual_delivery_mins - d.estimated_delivery_mins) AS delay_variance_mins,
    d.sla_status,
    d.weather_condition,
    d.traffic_level,
    d.delivery_rating
FROM deliveries d
JOIN orders o ON d.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN riders rd ON d.rider_id = rd.rider_id;


-- ----------------------------------------------------------------------------
-- 4. Stored Procedure: sp_GetMonthlyCityReport
-- Purpose: Dynamic operational query for territory managers to pull monthly reviews.
-- ----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_GetMonthlyCityReport;

DELIMITER $$
CREATE PROCEDURE sp_GetMonthlyCityReport(
    IN p_year INT,
    IN p_month INT,
    IN p_city VARCHAR(50)
)
BEGIN
    SELECT 
        p_city AS target_city,
        CONCAT(p_year, '-', LPAD(p_month, 2, '0')) AS report_period,
        COUNT(o.order_id) AS total_orders,
        SUM(CASE WHEN o.order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
        ROUND(SUM(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE 0 END), 2) AS total_gmv,
        ROUND(AVG(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE NULL END), 2) AS average_order_value,
        ROUND(SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id), 2) AS cancellation_rate_pct,
        ROUND(AVG(d.actual_delivery_mins), 1) AS avg_delivery_time_mins,
        ROUND(SUM(CASE WHEN d.sla_status = 'On-Time' THEN 1 ELSE 0 END) * 100.0 / COUNT(d.delivery_id), 2) AS sla_compliance_pct
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN deliveries d ON o.order_id = d.order_id
    WHERE YEAR(o.order_date) = p_year
      AND MONTH(o.order_date) = p_month
      AND (p_city IS NULL OR c.city = p_city);
END $$
DELIMITER ;