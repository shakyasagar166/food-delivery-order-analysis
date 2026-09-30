-- ============================================================================
-- Project: Food Delivery Order Analysis (Zomato / Swiggy Analytics Model)
-- File: 01_schema_setup.sql
-- Description: DDL script creating database, relational tables, constraints,
--              primary keys, foreign keys, and analytical performance indexes.
-- Target RDBMS: MySQL 8.0+
-- ============================================================================

DROP DATABASE IF EXISTS food_delivery_db;
CREATE DATABASE food_delivery_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE food_delivery_db;

-- ----------------------------------------------------------------------------
-- 1. Table: customers
-- ----------------------------------------------------------------------------
CREATE TABLE customers (
    customer_id VARCHAR(15) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    city VARCHAR(50) NOT NULL,
    signup_date DATE NOT NULL,
    customer_segment ENUM('Gold Member', 'Regular', 'Occasional') NOT NULL DEFAULT 'Regular',
    gender ENUM('Male', 'Female', 'Prefer Not to Say') DEFAULT 'Prefer Not to Say',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_customers PRIMARY KEY (customer_id)
) ENGINE=InnoDB;

CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_customers_segment ON customers(customer_segment);

-- ----------------------------------------------------------------------------
-- 2. Table: restaurants
-- ----------------------------------------------------------------------------
CREATE TABLE restaurants (
    restaurant_id VARCHAR(15) NOT NULL,
    restaurant_name VARCHAR(120) NOT NULL,
    city VARCHAR(50) NOT NULL,
    cuisine_type VARCHAR(50) NOT NULL,
    rating DECIMAL(2,1) NOT NULL CHECK (rating >= 1.0 AND rating <= 5.0),
    cost_for_two INT NOT NULL CHECK (cost_for_two > 0),
    commission_rate DECIMAL(3,2) NOT NULL DEFAULT 0.20,
    is_exclusive TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_restaurants PRIMARY KEY (restaurant_id)
) ENGINE=InnoDB;

CREATE INDEX idx_restaurants_city ON restaurants(city);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine_type);

-- ----------------------------------------------------------------------------
-- 3. Table: riders
-- ----------------------------------------------------------------------------
CREATE TABLE riders (
    rider_id VARCHAR(15) NOT NULL,
    rider_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    vehicle_type ENUM('Motorcycle', 'Electric Vehicle', 'Scooter') NOT NULL,
    rating DECIMAL(2,1) NOT NULL CHECK (rating >= 1.0 AND rating <= 5.0),
    joining_date DATE NOT NULL,
    status ENUM('Active', 'On Break', 'Inactive') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_riders PRIMARY KEY (rider_id)
) ENGINE=InnoDB;

CREATE INDEX idx_riders_city ON riders(city);
CREATE INDEX idx_riders_status ON riders(status);

-- ----------------------------------------------------------------------------
-- 4. Table: orders (Transaction Fact Header)
-- ----------------------------------------------------------------------------
CREATE TABLE orders (
    order_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(15) NOT NULL,
    restaurant_id VARCHAR(15) NOT NULL,
    rider_id VARCHAR(15) DEFAULT 'UNASSIGNED',
    order_date DATE NOT NULL,
    order_time TIME NOT NULL,
    order_timestamp DATETIME NOT NULL,
    order_status ENUM('Delivered', 'Cancelled', 'Refunded') NOT NULL,
    subtotal_amount DECIMAL(10,2) NOT NULL CHECK (subtotal_amount >= 0),
    discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    delivery_fee DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    platform_fee DECIMAL(10,2) NOT NULL DEFAULT 5.00,
    tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    cancellation_reason VARCHAR(100) DEFAULT 'N/A',
    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    CONSTRAINT fk_orders_restaurant FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_restaurant ON orders(restaurant_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(order_status);

-- ----------------------------------------------------------------------------
-- 5. Table: order_items (Transaction Line Items)
-- ----------------------------------------------------------------------------
CREATE TABLE order_items (
    order_item_id VARCHAR(20) NOT NULL,
    order_id VARCHAR(20) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    quantity INT NOT NULL CHECK (quantity > 0),
    total_price DECIMAL(10,2) NOT NULL CHECK (total_price >= 0),
    CONSTRAINT pk_order_items PRIMARY KEY (order_item_id),
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_items_order ON order_items(order_id);
CREATE INDEX idx_items_category ON order_items(category);

-- ----------------------------------------------------------------------------
-- 6. Table: deliveries (Fulfillment Fact Table)
-- ----------------------------------------------------------------------------
CREATE TABLE deliveries (
    delivery_id VARCHAR(20) NOT NULL,
    order_id VARCHAR(20) NOT NULL UNIQUE,
    rider_id VARCHAR(15) NOT NULL,
    pickup_timestamp DATETIME NOT NULL,
    delivery_timestamp DATETIME NOT NULL,
    distance_km DECIMAL(4,2) NOT NULL CHECK (distance_km > 0),
    estimated_delivery_mins INT NOT NULL CHECK (estimated_delivery_mins > 0),
    actual_delivery_mins INT NOT NULL CHECK (actual_delivery_mins > 0),
    sla_status ENUM('On-Time', 'Minor Delay (<15m)', 'Severe Breach (>15m)') NOT NULL,
    weather_condition ENUM('Clear', 'Rainy', 'Foggy', 'Extreme Heat') NOT NULL,
    traffic_level ENUM('Low', 'Moderate', 'Heavy', 'Gridlock') NOT NULL,
    delivery_rating DECIMAL(2,1) CHECK (delivery_rating >= 1.0 AND delivery_rating <= 5.0),
    CONSTRAINT pk_deliveries PRIMARY KEY (delivery_id),
    CONSTRAINT fk_delv_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_delv_rider FOREIGN KEY (rider_id) REFERENCES riders(rider_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE INDEX idx_deliveries_rider ON deliveries(rider_id);
CREATE INDEX idx_deliveries_sla ON deliveries(sla_status);
CREATE INDEX idx_deliveries_weather ON deliveries(weather_condition);

-- ----------------------------------------------------------------------------
-- 7. Table: payments (Payment Fact Table)
-- ----------------------------------------------------------------------------
CREATE TABLE payments (
    payment_id VARCHAR(20) NOT NULL,
    order_id VARCHAR(20) NOT NULL,
    payment_method VARCHAR(40) NOT NULL,
    payment_status ENUM('Successful', 'Failed', 'Refunded') NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL CHECK (amount_paid >= 0),
    payment_timestamp DATETIME NOT NULL,
    CONSTRAINT pk_payments PRIMARY KEY (payment_id),
    CONSTRAINT fk_pay_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(payment_status);
CREATE INDEX idx_payments_method ON payments(payment_method);