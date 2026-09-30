# Data Dictionary - Food Delivery Order Analysis

This document provides a comprehensive description of the relational database schema, data types, constraints, and business logic for the Food Delivery Analytics platform (Zomato / Swiggy / DoorDash model).

---

## 1. Table: `customers`
Stores demographic and registration details of platform users.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer_id` | `VARCHAR(15)` | No | **Primary Key** | Unique customer identifier | `CUST-0001` |
| `customer_name` | `VARCHAR(100)` | No | None | Full customer name | `Aarav Sharma` |
| `email` | `VARCHAR(120)` | No | Unique | Contact email address | `aarav.sharma@example.com` |
| `phone` | `VARCHAR(20)` | No | None | Contact mobile number | `+91-9876543210` |
| `city` | `VARCHAR(50)` | No | None | Operating metro city | `Bengaluru` |
| `signup_date` | `DATE` | No | None | Date of account creation | `2023-08-14` |
| `customer_segment`| `VARCHAR(20)` | No | None | Loyalty tier (`Gold Member`, `Regular`, `Occasional`) | `Gold Member` |
| `gender` | `VARCHAR(20)` | Yes | None | Demographic gender | `Male` |

---

## 2. Table: `restaurants`
Contains details of partner restaurants, cuisines, and commercial commission rates.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `restaurant_id` | `VARCHAR(15)` | No | **Primary Key** | Unique restaurant identifier | `REST-001` |
| `restaurant_name` | `VARCHAR(120)`| No | None | Registered outlet name | `Royal Dhaba (North)` |
| `city` | `VARCHAR(50)` | No | None | City location of outlet | `Mumbai` |
| `cuisine_type` | `VARCHAR(50)` | No | None | Primary cuisine category | `North Indian` |
| `rating` | `DECIMAL(2,1)`| No | None | Average customer review rating (1.0 to 5.0) | `4.6` |
| `cost_for_two` | `INT` | No | None | Approximate dining/ordering cost for 2 people (INR)| `600` |
| `commission_rate`| `DECIMAL(3,2)`| No | None | Platform take-rate percentage (e.g. 0.22 = 22%) | `0.22` |
| `is_exclusive` | `TINYINT(1)` | No | None | Exclusive platform partnership flag (1 = Yes, 0 = No)| `1` |

---

## 3. Table: `riders`
Fleet delivery personnel operational data.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `rider_id` | `VARCHAR(15)` | No | **Primary Key** | Unique delivery partner identifier | `RDR-001` |
| `rider_name` | `VARCHAR(100)` | No | None | Full name of rider | `Deepak Yadav` |
| `city` | `VARCHAR(50)` | No | None | Operating delivery zone/city | `Delhi NCR` |
| `vehicle_type` | `VARCHAR(30)` | No | None | Transportation mode (`Motorcycle`, `Electric Vehicle`, `Scooter`) | `Electric Vehicle` |
| `rating` | `DECIMAL(2,1)` | No | None | Historical delivery performance score (1.0 - 5.0) | `4.8` |
| `joining_date` | `DATE` | No | None | Onboarding date | `2023-09-10` |
| `status` | `VARCHAR(20)` | No | None | Current operational status (`Active`, `On Break`, `Inactive`) | `Active` |

---

## 4. Table: `orders`
Central transaction header fact table recording every order placement.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_id` | `VARCHAR(20)` | No | **Primary Key** | Unique order reference number | `ORD-20240001` |
| `customer_id` | `VARCHAR(15)` | No | **Foreign Key** (`customers.customer_id`) | ID of ordering customer | `CUST-0142` |
| `restaurant_id`| `VARCHAR(15)` | No | **Foreign Key** (`restaurants.restaurant_id`) | ID of preparing restaurant | `REST-019` |
| `rider_id` | `VARCHAR(15)` | Yes| **Foreign Key** (`riders.rider_id`) | Assigned delivery partner (`UNASSIGNED` if failed) | `RDR-045` |
| `order_date` | `DATE` | No | None | Date of order placement | `2024-03-15` |
| `order_time` | `TIME` | No | None | Time of order placement | `19:42:10` |
| `order_timestamp`| `DATETIME` | No | None | Full combined timestamp | `2024-03-15 19:42:10` |
| `order_status` | `VARCHAR(20)` | No | None | Status (`Delivered`, `Cancelled`, `Refunded`) | `Delivered` |
| `subtotal_amount`| `DECIMAL(10,2)`| No | None | Gross food items value before discounts (INR) | `760.00` |
| `discount_amount`| `DECIMAL(10,2)`| No | None | Promotional discount given (INR) | `114.00` |
| `delivery_fee` | `DECIMAL(10,2)`| No | None | Delivery surcharge billed to customer (INR) | `0.00` |
| `platform_fee` | `DECIMAL(10,2)`| No | None | Mandatory platform convenience fee (INR) | `5.00` |
| `tax_amount` | `DECIMAL(10,2)`| No | None | Goods & Services Tax (GST 5%) | `32.30` |
| `total_amount` | `DECIMAL(10,2)`| No | None | Net bill value paid by customer | `683.30` |
| `cancellation_reason` | `VARCHAR(100)`| Yes | None | Reason code if cancelled | `Late Rider Assignment` |

---

## 5. Table: `order_items`
Granular line-item breakdown of food dishes per order.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_item_id`| `VARCHAR(20)` | No | **Primary Key** | Unique line item reference | `ITEM-000001` |
| `order_id` | `VARCHAR(20)` | No | **Foreign Key** (`orders.order_id`) | Parent order reference | `ORD-20240001` |
| `item_name` | `VARCHAR(100)` | No | None | Name of dish/product | `Hyderabadi Chicken Dum Biryani` |
| `category` | `VARCHAR(50)` | No | None | Dish group (`Main Course`, `Appetizer`, `Dessert`, etc.) | `Main Course` |
| `unit_price` | `DECIMAL(10,2)`| No | None | Price per unit item | `330.00` |
| `quantity` | `INT` | No | None | Quantity ordered | `2` |
| `total_price` | `DECIMAL(10,2)`| No | None | Line item total (`unit_price * quantity`) | `660.00` |

---

## 6. Table: `deliveries`
Fulfillment and logistics telemetry tracking trip performance, SLAs, and external variables.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `delivery_id` | `VARCHAR(20)` | No | **Primary Key** | Unique fulfillment delivery record | `DELV-00001` |
| `order_id` | `VARCHAR(20)` | No | **Foreign Key** (`orders.order_id`) | Linked order | `ORD-20240001` |
| `rider_id` | `VARCHAR(15)` | No | **Foreign Key** (`riders.rider_id`) | Assigned driver | `RDR-045` |
| `pickup_timestamp` | `DATETIME` | No | None | Timestamp when rider collected food from restaurant | `2024-03-15 19:58:00` |
| `delivery_timestamp`| `DATETIME` | No | None | Timestamp when order arrived at customer doorstep | `2024-03-15 20:25:00` |
| `distance_km` | `DECIMAL(4,2)` | No | None | Travel distance between restaurant and customer (km) | `5.40` |
| `estimated_delivery_mins` | `INT` | No | None | System predicted ETA at order creation (mins) | `30` |
| `actual_delivery_mins` | `INT` | No | None | Actual trip duration from order to doorstep (mins) | `43` |
| `sla_status` | `VARCHAR(30)` | No | None | Service Level Agreement classification (`On-Time`, `Minor Delay (<15m)`, `Severe Breach (>15m)`) | `Minor Delay (<15m)` |
| `weather_condition` | `VARCHAR(30)` | No | None | Weather during delivery (`Clear`, `Rainy`, `Foggy`, `Extreme Heat`) | `Rainy` |
| `traffic_level` | `VARCHAR(30)` | No | None | Road congestion status (`Low`, `Moderate`, `Heavy`, `Gridlock`) | `Heavy` |
| `delivery_rating` | `DECIMAL(2,1)` | Yes | None | Rider rating submitted by customer (1.0 to 5.0) | `3.5` |

---

## 7. Table: `payments`
Financial reconciliation table tracking checkout transactions.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `payment_id` | `VARCHAR(20)` | No | **Primary Key** | Unique payment transaction record | `PAY-00001` |
| `order_id` | `VARCHAR(20)` | No | **Foreign Key** (`orders.order_id`) | Linked order ID | `ORD-20240001` |
| `payment_method`| `VARCHAR(40)` | No | None | Payment channel (`UPI / GPay / PhonePe`, `Credit Card`, `Debit Card`, `Cash on Delivery`, `Digital Wallet`) | `UPI / GPay / PhonePe` |
| `payment_status`| `VARCHAR(20)` | No | None | Settlement state (`Successful`, `Failed`, `Refunded`)| `Successful` |
| `amount_paid` | `DECIMAL(10,2)`| No | None | Amount debited or credited (INR) | `683.30` |
| `payment_timestamp`| `DATETIME` | No | None | Gateway transaction timestamp | `2024-03-15 19:43:25` |

---

## Entity Relationship Summary (Star / Snowflake Schema)
- `orders` is the central **Transaction Fact Table**.
- `deliveries` acts as the **Logistics / Fulfillment Fact Table**.
- `order_items` acts as the **Line-Item Dimension / Bridge Table**.
- `customers`, `restaurants`, `riders` serve as the primary **Dimension Tables**.
- Temporal slicing is supported natively via `order_date`, `pickup_timestamp`, and `delivery_timestamp`.