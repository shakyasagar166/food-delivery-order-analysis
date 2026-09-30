-- ============================================================================
-- Project: Food Delivery Order Analysis (Zomato / Swiggy Business Analyst Project)
-- File: 03_business_queries.sql
-- Description: 21 In-Depth Analytical SQL Queries answering strategic business
--              problems across Executive KPIs, Revenue, Operations, and Customers.
-- ============================================================================

USE food_delivery_db;

-- ============================================================================
-- SECTION 1: EXECUTIVE KPIs & PLATFORM HEALTH
-- ============================================================================

-- Query 1: Platform High-Level Executive Summary
-- Purpose: Calculate total GMV, Net Revenue, Delivered Volume, AOV, and Discount Cost.
SELECT 
    COUNT(order_id) AS total_orders_placed,
    SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN total_amount ELSE 0 END), 2) AS total_delivered_gmv,
    ROUND(AVG(CASE WHEN order_status = 'Delivered' THEN total_amount ELSE NULL END), 2) AS average_order_value_aov,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN discount_amount ELSE 0 END), 2) AS total_discounts_subsidized,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN platform_fee ELSE 0 END), 2) AS total_platform_fee_collected,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 2) AS fulfillment_rate_pct
FROM orders;


-- Query 2: Order Fulfillment Funnel & Status Breakdown
-- Purpose: Quantify drop-off and cancellation rates for operational review.
SELECT 
    order_status,
    COUNT(order_id) AS total_orders,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage_share,
    ROUND(SUM(total_amount), 2) AS gross_impact_value
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- Query 3: City-Wise Revenue & Market Penetration Performance
-- Purpose: Compare metro markets on volume, average ticket size, and customer density.
SELECT 
    c.city,
    COUNT(DISTINCT c.customer_id) AS total_registered_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE 0 END), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE NULL END), 2) AS city_aov,
    ROUND(SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id), 2) AS cancellation_rate_pct
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;


-- ============================================================================
-- SECTION 2: REVENUE, RESTAURANT & CUISINE ANALYTICS
-- ============================================================================

-- Query 4: Monthly Revenue Trend and Month-over-Month (MoM) Growth %
-- Purpose: Track commercial trajectory using the LAG() window function.
WITH MonthlyRevenue AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS order_month,
        COUNT(order_id) AS total_monthly_orders,
        ROUND(SUM(total_amount), 2) AS monthly_net_gmv
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    order_month,
    total_monthly_orders,
    monthly_net_gmv,
    LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month) AS previous_month_gmv,
    ROUND(
        (monthly_net_gmv - LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month)) * 100.0 / 
        LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month), 
        2
    ) AS mom_growth_pct
FROM MonthlyRevenue;


-- Query 5: Top 3 Revenue Generating Restaurants in Each City
-- Purpose: Identify regional flagship partners using DENSE_RANK() window function.
WITH RankedRestaurants AS (
    SELECT 
        r.city,
        r.restaurant_name,
        r.cuisine_type,
        r.rating,
        COUNT(o.order_id) AS total_delivered_orders,
        ROUND(SUM(o.total_amount), 2) AS gross_sales,
        ROUND(SUM(o.total_amount * r.commission_rate), 2) AS platform_commission_earned,
        DENSE_RANK() OVER (PARTITION BY r.city ORDER BY SUM(o.total_amount) DESC) AS rank_in_city
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE o.order_status = 'Delivered'
    GROUP BY r.city, r.restaurant_id, r.restaurant_name, r.cuisine_type, r.rating, r.commission_rate
)
SELECT *
FROM RankedRestaurants
WHERE rank_in_city <= 3
ORDER BY city, rank_in_city;


-- Query 6: Cuisine Popularity, Share of Wallet, and Take-Rate Profitability
-- Purpose: Evaluate which cuisine drives the highest platform commission vs order volume.
SELECT 
    r.cuisine_type,
    COUNT(DISTINCT r.restaurant_id) AS active_restaurants,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_gmv,
    ROUND(AVG(o.total_amount), 2) AS avg_cuisine_ticket_size,
    ROUND(SUM(o.total_amount * r.commission_rate), 2) AS net_platform_commission,
    ROUND(SUM(o.total_amount) * 100.0 / (SELECT SUM(total_amount) FROM orders WHERE order_status = 'Delivered'), 2) AS gmv_share_pct
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.cuisine_type
ORDER BY total_gmv DESC;


-- Query 7: High Volume but Low-Rated Restaurants (Quality Hazard Audit)
-- Purpose: Flag high-demand restaurants whose subpar rating hurts customer retention.
SELECT 
    restaurant_name,
    city,
    cuisine_type,
    rating,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS gmv_generated
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, restaurant_name, city, cuisine_type, rating
HAVING total_orders >= 50 AND rating < 3.8
ORDER BY total_orders DESC;


-- ============================================================================
-- SECTION 3: OPERATIONS, LOGISTICS & DELIVERY SLA BREACHES
-- ============================================================================

-- Query 8: Platform On-Time Delivery Rate & SLA Compliance
-- Purpose: Measure operational efficiency against SLA targets.
SELECT 
    sla_status,
    COUNT(delivery_id) AS total_trips,
    ROUND(COUNT(delivery_id) * 100.0 / (SELECT COUNT(*) FROM deliveries), 2) AS compliance_rate_pct,
    ROUND(AVG(actual_delivery_mins), 1) AS avg_duration_mins,
    ROUND(AVG(delivery_rating), 2) AS avg_customer_rating
FROM deliveries
GROUP BY sla_status
ORDER BY total_trips DESC;


-- Query 9: Impact of Weather and Road Congestion on Delivery Delays
-- Purpose: Quantify environmental friction on delivery times to refine dynamic ETAs.
SELECT 
    weather_condition,
    traffic_level,
    COUNT(delivery_id) AS trip_volume,
    ROUND(AVG(actual_delivery_mins), 1) AS avg_trip_time_mins,
    ROUND(AVG(estimated_delivery_mins), 1) AS avg_estimated_mins,
    ROUND(AVG(actual_delivery_mins - estimated_delivery_mins), 1) AS avg_delay_variance_mins,
    ROUND(SUM(CASE WHEN sla_status = 'Severe Breach (>15m)' THEN 1 ELSE 0 END) * 100.0 / COUNT(delivery_id), 2) AS severe_breach_rate_pct
FROM deliveries
GROUP BY weather_condition, traffic_level
ORDER BY avg_trip_time_mins DESC;


-- Query 10: Trip Distance Bucketing vs SLA Adherence
-- Purpose: Determine threshold distance where SLA breach rate accelerates.
SELECT 
    CASE 
        WHEN distance_km < 3.0 THEN '1. Hyperlocal (< 3 km)'
        WHEN distance_km BETWEEN 3.0 AND 6.99 THEN '2. Short (3 - 7 km)'
        WHEN distance_km BETWEEN 7.0 AND 11.99 THEN '3. Medium (7 - 12 km)'
        ELSE '4. Long Distance (> 12 km)'
    END AS distance_bucket,
    COUNT(delivery_id) AS total_deliveries,
    ROUND(AVG(distance_km), 2) AS avg_distance,
    ROUND(AVG(actual_delivery_mins), 1) AS avg_delivery_time_mins,
    ROUND(SUM(CASE WHEN sla_status = 'On-Time' THEN 1 ELSE 0 END) * 100.0 / COUNT(delivery_id), 2) AS on_time_percentage
FROM deliveries
GROUP BY distance_bucket
ORDER BY distance_bucket;


-- Query 11: Top 10 Delivery Partners by Efficiency & Quality Score
-- Purpose: Identify top riders for incentive bonus allocation.
SELECT 
    r.rider_id,
    r.rider_name,
    r.city,
    r.vehicle_type,
    COUNT(d.delivery_id) AS total_orders_fulfilled,
    ROUND(AVG(d.actual_delivery_mins), 1) AS avg_mins_per_trip,
    ROUND(SUM(CASE WHEN d.sla_status = 'On-Time' THEN 1 ELSE 0 END) * 100.0 / COUNT(d.delivery_id), 2) AS rider_sla_compliance_pct,
    ROUND(AVG(d.delivery_rating), 2) AS avg_customer_rating
FROM riders r
JOIN deliveries d ON r.rider_id = d.rider_id
GROUP BY r.rider_id, r.rider_name, r.city, r.vehicle_type
HAVING total_orders_fulfilled >= 25
ORDER BY rider_sla_compliance_pct DESC, avg_customer_rating DESC
LIMIT 10;


-- Query 12: Peak Ordering Hours and Fulfillment Speed
-- Purpose: Identify rush hours (Lunch vs Dinner) for fleet surge planning.
SELECT 
    HOUR(order_time) AS hour_of_day,
    CASE 
        WHEN HOUR(order_time) BETWEEN 11 AND 15 THEN 'Lunch Peak'
        WHEN HOUR(order_time) BETWEEN 19 AND 23 THEN 'Dinner Peak'
        ELSE 'Off-Peak / Evening Snacks'
    END AS time_band,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS gmv_in_hour,
    ROUND(AVG(d.actual_delivery_mins), 1) AS avg_fulfillment_time_mins,
    ROUND(SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id), 2) AS hourly_cancel_rate_pct
FROM orders o
LEFT JOIN deliveries d ON o.order_id = d.order_id
GROUP BY HOUR(order_time), time_band
ORDER BY hour_of_day;


-- ============================================================================
-- SECTION 4: CUSTOMER SEGMENTATION, RFM & COHORT RETENTION
-- ============================================================================

-- Query 13: Customer RFM Scoring Model (Recency, Frequency, Monetary)
-- Purpose: Classify customers into Champions, Loyalists, Potential Churn, and Inactive.
WITH CustomerMetrics AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.customer_segment,
        DATEDIFF('2024-12-31', MAX(o.order_date)) AS recency_days,
        COUNT(o.order_id) AS order_frequency,
        ROUND(SUM(o.total_amount), 2) AS monetary_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'Delivered'
    GROUP BY c.customer_id, c.customer_name, c.customer_segment
),
RFMTiles AS (
    SELECT 
        customer_id,
        customer_name,
        customer_segment,
        recency_days,
        order_frequency,
        monetary_value,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,   -- 4 = Most Recent
        NTILE(4) OVER (ORDER BY order_frequency ASC) AS f_score, -- 4 = Highest Frequency
        NTILE(4) OVER (ORDER BY monetary_value ASC) AS m_score   -- 4 = Highest Spend
    FROM CustomerMetrics
)
SELECT 
    customer_id,
    customer_name,
    customer_segment,
    recency_days,
    order_frequency,
    monetary_value,
    (r_score + f_score + m_score) AS composite_rfm_score,
    CASE 
        WHEN (r_score + f_score + m_score) >= 10 THEN 'VIP Champion'
        WHEN (r_score + f_score + m_score) >= 7 THEN 'Loyal Customer'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At-Risk / Needs Re-engagement'
        ELSE 'Low Engagement / Churn Candidate'
    END AS rfm_behavioral_persona
FROM RFMTiles
ORDER BY composite_rfm_score DESC
LIMIT 20;


-- Query 14: Customer Lifetime Value (LTV) across Loyalty Segments
-- Purpose: Evaluate Gold Member economics vs Regular customers.
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(o.order_id) AS total_orders,
    ROUND(COUNT(o.order_id) * 1.0 / COUNT(DISTINCT c.customer_id), 1) AS orders_per_customer,
    ROUND(SUM(o.total_amount), 2) AS total_segment_spend,
    ROUND(AVG(o.total_amount), 2) AS segment_aov,
    ROUND(SUM(o.discount_amount), 2) AS total_discounts_granted,
    ROUND(SUM(o.delivery_fee), 2) AS total_delivery_fee_collected
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status = 'Delivered'
GROUP BY c.customer_segment
ORDER BY total_segment_spend DESC;


-- Query 15: Repeat Order Frequency Distribution
-- Purpose: Understand the % of users who place multiple orders vs one-and-done users.
WITH OrderCounts AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS order_count
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN order_count = 1 THEN '1 Order (One-and-Done)'
        WHEN order_count BETWEEN 2 AND 4 THEN '2 - 4 Orders (Developing)'
        WHEN order_count BETWEEN 5 AND 9 THEN '5 - 9 Orders (Frequent)'
        ELSE '10+ Orders (Super Users)'
    END AS user_cohort_frequency,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM OrderCounts), 2) AS customer_percentage
FROM OrderCounts
GROUP BY user_cohort_frequency
ORDER BY customer_count DESC;


-- Query 16: Monthly Customer Retention Cohort Analysis
-- Purpose: Cohort analysis tracking monthly order activity from initial acquisition.
WITH CustomerCohort AS (
    SELECT 
        customer_id,
        DATE_FORMAT(MIN(order_date), '%Y-%m') AS cohort_month
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
),
CohortActivity AS (
    SELECT 
        cc.cohort_month,
        DATE_FORMAT(o.order_date, '%Y-%m') AS activity_month,
        COUNT(DISTINCT o.customer_id) AS active_users
    FROM orders o
    JOIN CustomerCohort cc ON o.customer_id = cc.customer_id
    WHERE o.order_status = 'Delivered'
    GROUP BY cc.cohort_month, DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT 
    cohort_month,
    activity_month,
    active_users
FROM CohortActivity
ORDER BY cohort_month, activity_month;


-- ============================================================================
-- SECTION 5: CANCELLATIONS, DISCOUNTS & FINANCIAL RECONCILIATION
-- ============================================================================

-- Query 17: Root Cause Analysis of Order Cancellations
-- Purpose: Diagnose key bottlenecks causing lost revenue.
SELECT 
    cancellation_reason,
    COUNT(order_id) AS cancelled_orders,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM orders WHERE order_status = 'Cancelled'), 2) AS pct_of_cancellations,
    ROUND(SUM(subtotal_amount), 2) AS lost_merchandise_value
FROM orders
WHERE order_status = 'Cancelled'
GROUP BY cancellation_reason
ORDER BY cancelled_orders DESC;


-- Query 18: Payment Gateway Reliability & Method Distribution
-- Purpose: Audit checkout failure rate across payment methods.
SELECT 
    payment_method,
    COUNT(payment_id) AS total_transactions,
    ROUND(SUM(CASE WHEN payment_status = 'Successful' THEN 1 ELSE 0 END) * 100.0 / COUNT(payment_id), 2) AS success_rate_pct,
    ROUND(SUM(CASE WHEN payment_status = 'Failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(payment_id), 2) AS failure_rate_pct,
    ROUND(SUM(amount_paid), 2) AS total_transacted_volume
FROM payments
GROUP BY payment_method
ORDER BY total_transactions DESC;


-- Query 19: Running Cumulative Platform Revenue by City (Window Function)
-- Purpose: Visualize cumulative revenue accumulation over calendar months.
WITH DailyCitySales AS (
    SELECT 
        c.city,
        o.order_date,
        SUM(o.total_amount) AS daily_sales
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'Delivered'
    GROUP BY c.city, o.order_date
)
SELECT 
    city,
    order_date,
    ROUND(daily_sales, 2) AS daily_sales,
    ROUND(SUM(daily_sales) OVER (PARTITION BY city ORDER BY order_date), 2) AS cumulative_city_revenue
FROM DailyCitySales
ORDER BY city, order_date;


-- Query 20: Top 10 Best-Selling Menu Dishes Across All Platforms
-- Purpose: Identify hero food items and their total revenue contribution.
SELECT 
    oi.item_name,
    oi.category,
    COUNT(DISTINCT oi.order_id) AS times_ordered,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.total_price), 2) AS gross_revenue_generated
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY oi.item_name, oi.category
ORDER BY total_units_sold DESC
LIMIT 10;


-- Query 21: Financial Leakage Audit: Discount vs Commission Rate Analysis
-- Purpose: Identify restaurants where platform discount exceeded commission earnings.
SELECT 
    r.restaurant_id,
    r.restaurant_name,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount * r.commission_rate), 2) AS total_commission_earned,
    ROUND(SUM(o.discount_amount), 2) AS total_discount_subsidized,
    ROUND(SUM(o.total_amount * r.commission_rate) - SUM(o.discount_amount), 2) AS net_platform_contribution
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_id, r.restaurant_name, r.commission_rate
ORDER BY net_platform_contribution ASC
LIMIT 10;