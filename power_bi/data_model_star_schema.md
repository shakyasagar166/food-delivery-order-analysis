# Power BI Star Schema Data Model Architecture

An optimized dimensional model (Star / Constellation Schema) engineered for high performance, fast query processing in VertiPaq, and intuitive DAX measure calculations.

---

## 1. Schema Architecture Diagram

```
                 +-------------------+
                 |    Dim_Customer   |
                 +-------------------+
                 | * customer_id (PK)|
                 |   customer_name   |
                 |   city            |
                 |   customer_segment|
                 |   signup_date     |
                 +---------+---------+
                           | 1
                           | 
                           | *
+-------------------+      |      +---------------------+
|    Dim_Date       |      |      |   Dim_Restaurant    |
+-------------------+      |      +---------------------+
| * Date (PK)       |      |      | * restaurant_id (PK)|
|   Year            |      |      |   restaurant_name   |
|   Month / MonthNo |      |      |   city              |
|   Quarter         |      |      |   cuisine_type      |
|   DayOfWeek       |      |      |   rating            |
|   IsWeekend       |      |      |   commission_rate   |
+---------+---------+      |      +----------+----------+
          | 1              |                 | 1
          |                |                 |
          | *              |                 | *
+---------+----------------+-----------------+----------+
|                       Fact_Orders                     |
+-------------------------------------------------------+
| * order_id (PK)                                       |
|   customer_id (FK) -> Dim_Customer                    |
|   restaurant_id (FK) -> Dim_Restaurant                |
|   rider_id (FK) -> Dim_Rider                          |
|   order_date (FK) -> Dim_Date                         |
|   order_time                                          |
|   order_status                                        |
|   subtotal_amount                                     |
|   discount_amount                                     |
|   delivery_fee                                        |
|   platform_fee                                        |
|   tax_amount                                          |
|   total_amount                                        |
|   cancellation_reason                                 |
+---------------------------+---------------------------+
                            | 1
                            |
                            | 1 (or 1:*)
+---------------------------+---------------------------+
|                      Fact_Deliveries                  |
+-------------------------------------------------------+
| * delivery_id (PK)                                    |
|   order_id (FK) -> Fact_Orders                        |
|   rider_id (FK) -> Dim_Rider                          |
|   pickup_timestamp                                    |
|   delivery_timestamp                                  |
|   distance_km                                         |
|   estimated_delivery_mins                             |
|   actual_delivery_mins                                |
|   sla_status                                          |
|   weather_condition                                   |
|   traffic_level                                       |
|   delivery_rating                                     |
+---------------------------+---------------------------+
                            | *
                            |
                            | 1
                 +----------+--------+
                 |     Dim_Rider     |
                 +-------------------+
                 | * rider_id (PK)   |
                 |   rider_name      |
                 |   city            |
                 |   vehicle_type    |
                 |   rating          |
                 |   status          |
                 +-------------------+
```

---

## 2. Table Relationships & Cardinalities

| From Table (Primary/Dimension) | To Table (Foreign/Fact) | Primary Key | Foreign Key | Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Dim_Customer` | `Fact_Orders` | `customer_id` | `customer_id` | One-to-Many (`1:*`) | Single (`Dim_Customer` filters `Fact_Orders`) |
| `Dim_Restaurant` | `Fact_Orders` | `restaurant_id` | `restaurant_id` | One-to-Many (`1:*`) | Single (`Dim_Restaurant` filters `Fact_Orders`) |
| `Dim_Rider` | `Fact_Orders` | `rider_id` | `rider_id` | One-to-Many (`1:*`) | Single (`Dim_Rider` filters `Fact_Orders`) |
| `Dim_Date` | `Fact_Orders` | `Date` | `order_date` | One-to-Many (`1:*`) | Single (`Dim_Date` filters `Fact_Orders`) |
| `Dim_Rider` | `Fact_Deliveries` | `rider_id` | `rider_id` | One-to-Many (`1:*`) | Single (`Dim_Rider` filters `Fact_Deliveries`) |
| `Fact_Orders` | `Fact_Deliveries` | `order_id` | `order_id` | One-to-One / Many (`1:1` or `1:*`)| Both (Allows bi-directional slicers) |

---

## 3. Dedicated Date Dimension (DAX Calendar Table)

Create a contiguous Date Dimension in Power BI to enable Time Intelligence functions (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`):

```dax
Dim_Date = 
VAR MinDate = MIN(Fact_Orders[order_date])
VAR MaxDate = MAX(Fact_Orders[order_date])
RETURN
    ADDCOLUMNS (
        CALENDAR (MinDate, MaxDate),
        "Year", YEAR([Date]),
        "Year-Month", FORMAT([Date], "YYYY-MM"),
        "Month Name", FORMAT([Date], "MMMM"),
        "Month Short", FORMAT([Date], "MMM"),
        "Month Number", MONTH([Date]),
        "Quarter", "Q" & FORMAT([Date], "Q"),
        "Day of Week", FORMAT([Date], "dddd"),
        "Day of Week No", WEEKDAY([Date], 2),
        "Is Weekend", IF(WEEKDAY([Date], 2) >= 6, "Weekend", "Weekday")
    )
```

> **Configuration Tip**: Select `Month Name` column $\rightarrow$ In the Column Tools ribbon, click **Sort by Column** $\rightarrow$ Select `Month Number` to prevent alphabetical month sorting.