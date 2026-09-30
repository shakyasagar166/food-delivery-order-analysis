-- ============================================================================
-- Project: Food Delivery Order Analysis
-- File: 02_data_ingestion.sql
-- Description: Bulk loading script to ingest CSV files into MySQL tables.
-- ============================================================================

USE food_delivery_db;

-- Step 1: Enable local infile loading if restricted
SET GLOBAL local_infile = 1;

-- Note: Adjust the filepath below to match your local machine directory:
-- Example Windows Path: 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/customers.csv'

-- ----------------------------------------------------------------------------
-- 1. Ingest Customers
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(customer_id, customer_name, email, phone, city, signup_date, customer_segment, gender);

-- ----------------------------------------------------------------------------
-- 2. Ingest Restaurants
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/restaurants.csv'
INTO TABLE restaurants
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(restaurant_id, restaurant_name, city, cuisine_type, rating, cost_for_two, commission_rate, is_exclusive);

-- ----------------------------------------------------------------------------
-- 3. Ingest Riders
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/riders.csv'
INTO TABLE riders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(rider_id, rider_name, city, vehicle_type, rating, joining_date, status);

-- ----------------------------------------------------------------------------
-- 4. Ingest Orders
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(order_id, customer_id, restaurant_id, rider_id, order_date, order_time, order_timestamp, order_status, subtotal_amount, discount_amount, delivery_fee, platform_fee, tax_amount, total_amount, cancellation_reason);

-- ----------------------------------------------------------------------------
-- 5. Ingest Order Items
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/order_items.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(order_item_id, order_id, item_name, category, unit_price, quantity, total_price);

-- ----------------------------------------------------------------------------
-- 6. Ingest Deliveries
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/deliveries.csv'
INTO TABLE deliveries
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(delivery_id, order_id, rider_id, pickup_timestamp, delivery_timestamp, distance_km, estimated_delivery_mins, actual_delivery_mins, sla_status, weather_condition, traffic_level, delivery_rating);

-- ----------------------------------------------------------------------------
-- 7. Ingest Payments
-- ----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE 'C:/Users/Asus/.gemini/antigravity/scratch/food-delivery-order-analysis/data/raw/payments.csv'
INTO TABLE payments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(payment_id, order_id, payment_method, payment_status, amount_paid, payment_timestamp);

-- ----------------------------------------------------------------------------
-- Verification Queries (Run to confirm row ingestion counts)
-- ----------------------------------------------------------------------------
SELECT 'customers' AS table_name, COUNT(*) AS total_rows FROM customers
UNION ALL
SELECT 'restaurants', COUNT(*) FROM restaurants
UNION ALL
SELECT 'riders', COUNT(*) FROM riders
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'deliveries', COUNT(*) FROM deliveries
UNION ALL
SELECT 'payments', COUNT(*) FROM payments;