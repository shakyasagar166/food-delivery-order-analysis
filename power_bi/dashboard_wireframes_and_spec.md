# Power BI Report Wireframe & Dashboard Specifications

This document outlines the visual structure, layout grid, slicers, charts, and interaction design for the 3-Page Power BI Executive Report.

---

## Canvas Settings & Theme Palette
- **Canvas Size**: 16:9 widescreen (1280 x 720 px)
- **Background Color**: `#F8FAFC` (Slate Light Gray)
- **Card Background**: `#FFFFFF` with soft drop shadow (`blur: 4px, opacity: 10%`)
- **Primary Color (Headers / Dark)**: `#1E293B`
- **Secondary Accent (Teal / Primary KPI)**: `#0D9488`
- **Gold Accent (VIP / Highlights)**: `#F59E0B`
- **Positive / SLA On-Time**: `#10B981`
- **Negative / Breaches / Cancellations**: `#EF4444`

---

## PAGE 1: EXECUTIVE OVERVIEW (Strategic Performance)

### Layout Grid:
```
+------------------------------------------------------------------------------------+
| [Logo] Food Delivery Platform Executive Cockpit     [Slicers: Year | City | Segment]|
+------------------------------------------------------------------------------------+
| [Card: Net GMV]  [Card: Delivered Orders]  [Card: AOV]  [Card: SLA %] [Card: Cancel %]|
+--------------------------------------------------+---------------------------------+
| Visual 1: Monthly GMV & MoM Growth %            | Visual 2: GMV Share by City     |
| (Line and Clustered Column Chart)                | (Donut / Treemap Chart)         |
| - X-Axis: Dim_Date[Year-Month]                   | - Category: Dim_Customer[city]  |
| - Column: [Net Delivered GMV]                    | - Values: [Net Delivered GMV]   |
| - Line: [MoM GMV Growth %]                       |                                 |
+--------------------------------------------------+---------------------------------+
| Visual 3: Top 10 Restaurants by Net Revenue      | Visual 4: Cuisine Breakdown     |
| (Horizontal Clustered Bar Chart)                 | (Clustered Bar Chart)           |
| - Y-Axis: Dim_Restaurant[restaurant_name]        | - Y-Axis: cuisine_type          |
| - X-Axis: [Net Delivered GMV]                    | - X-Axis: [Net Delivered GMV]   |
| - Tooltip: [Delivered Orders], [AOV], Rating     | - Data Color: by Margin/Take-Rt |
+------------------------------------------------------------------------------------+
```

---

## PAGE 2: OPERATIONS & LOGISTICS SLA (Fleet & Fulfillment)

### Layout Grid:
```
+------------------------------------------------------------------------------------+
| Operations & Delivery SLA Audit                     [Slicers: Weather | Traffic]   |
+------------------------------------------------------------------------------------+
| [Card: Avg Trip Mins]  [Card: SLA Compliance %]  [Card: Severe Breaches] [Rider Rating]|
+--------------------------------------------------+---------------------------------+
| Visual 1: Actual vs Estimated Time by Distance   | Visual 2: Weather & Traffic     |
| (Scatter / Line Chart)                           | SLA Breach Heatmap (Matrix)     |
| - X-Axis: Distance Buckets (<3km, 3-7km, >7km)  | - Rows: weather_condition       |
| - Series 1: [Avg Delivery Duration (Mins)]       | - Columns: traffic_level        |
| - Series 2: [Avg Estimated ETA (Mins)]           | - Values: [SLA Compliance Rate%]|
+--------------------------------------------------+---------------------------------+
| Visual 3: Peak Hour Delivery Duration Bottleneck | Visual 4: Rider Leaderboard     |
| (Area Chart)                                     | (Table Visual)                  |
| - X-Axis: Hour of Day (11 to 23)                 | - Dim_Rider[rider_name]         |
| - Y-Axis: [Avg Delivery Duration (Mins)]         | - [Total Deliveries Completed]  |
| - Secondary Line: [Total Orders Placed]          | - [SLA Compliance Rate %]       |
|                                                  | - [Avg Delivery Rating]         |
+------------------------------------------------------------------------------------+
```

---

## PAGE 3: CUSTOMER INTELLIGENCE & SEGMENTATION (RFM & Retention)

### Layout Grid:
```
+------------------------------------------------------------------------------------+
| Customer Behavioral Personas & Retention            [Slicers: Customer Segment]    |
+------------------------------------------------------------------------------------+
| [Card: Active Users] [Card: ARPU] [Card: Gold Share %] [Card: Repeat Purchase Rate %]|
+--------------------------------------------------+---------------------------------+
| Visual 1: Customer Frequency Distribution        | Visual 2: Spend & Orders by Tier|
| (Column Chart)                                   | (100% Stacked Bar Chart)        |
| - Buckets: 1 Order, 2-4 Orders, 5-9, 10+ Orders  | - Axis: customer_segment        |
| - Values: [Active Transacting Customers]         | - Metric: GMV vs Discount Given |
+--------------------------------------------------+---------------------------------+
| Visual 3: Order Cancellation Root Causes         | Visual 4: Payment Funnel Audit  |
| (Funnel / Horizontal Bar Chart)                  | (Donut Chart)                   |
| - Categories: cancellation_reason                | - Dim_Payment[payment_method]   |
| - Values: [Cancelled Orders]                     | - Values: [Successful Volume]   |
| - Tooltip: [Lost Revenue (Cancellations)]        | - Filter: Failed vs Successful  |
+------------------------------------------------------------------------------------+
```