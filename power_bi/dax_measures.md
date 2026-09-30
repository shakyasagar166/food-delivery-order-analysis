# Production DAX Measures Library - Food Delivery Order Analysis

This library provides 30+ categorized, tested DAX measures for Power BI reports. Create a dedicated empty table named `_Measures` in Power BI to house these calculations.

---

## 1. Core Financial & Volume Measures

### Measure 1: Total Orders Placed
```dax
[Total Orders Placed] = 
COUNTROWS(Fact_Orders)
```
- **Format**: Whole Number (`#,##0`)

### Measure 2: Delivered Orders Volume
```dax
[Delivered Orders] = 
CALCULATE(
    COUNTROWS(Fact_Orders),
    Fact_Orders[order_status] = "Delivered"
)
```

### Measure 3: Cancelled Orders Volume
```dax
[Cancelled Orders] = 
CALCULATE(
    COUNTROWS(Fact_Orders),
    Fact_Orders[order_status] = "Cancelled"
)
```

### Measure 4: Gross Merchandise Value (GMV)
```dax
[Gross GMV] = 
SUM(Fact_Orders[subtotal_amount])
```
- **Format**: Currency (`₹ #,##0.00`)

### Measure 5: Delivered Net GMV (Billed Revenue)
```dax
[Net Delivered GMV] = 
CALCULATE(
    SUM(Fact_Orders[total_amount]),
    Fact_Orders[order_status] = "Delivered"
)
```

### Measure 6: Total Promotional Discounts Subsidized
```dax
[Total Discounts Given] = 
CALCULATE(
    SUM(Fact_Orders[discount_amount]),
    Fact_Orders[order_status] = "Delivered"
)
```

### Measure 7: Platform Take-Rate Revenue (Commissions + Platform Fees)
```dax
[Platform Take-Rate Revenue] = 
CALCULATE(
    SUMX(
        Fact_Orders,
        Fact_Orders[subtotal_amount] * RELATED(Dim_Restaurant[commission_rate]) + Fact_Orders[platform_fee]
    ),
    Fact_Orders[order_status] = "Delivered"
)
```

### Measure 8: Average Order Value (AOV)
```dax
[AOV] = 
DIVIDE(
    [Net Delivered GMV],
    [Delivered Orders],
    0
)
```

### Measure 9: Order Cancellation Rate %
```dax
[Cancellation Rate %] = 
DIVIDE(
    [Cancelled Orders],
    [Total Orders Placed],
    0
)
```
- **Format**: Percentage (`0.0%`)

---

## 2. Operations & Logistics SLA Measures

### Measure 10: Total Deliveries Completed
```dax
[Total Deliveries Completed] = 
COUNTROWS(Fact_Deliveries)
```

### Measure 11: On-Time Deliveries Count
```dax
[On-Time Deliveries] = 
CALCULATE(
    COUNTROWS(Fact_Deliveries),
    Fact_Deliveries[sla_status] = "On-Time"
)
```

### Measure 12: SLA Compliance Rate % (On-Time Delivery %)
```dax
[SLA Compliance Rate %] = 
DIVIDE(
    [On-Time Deliveries],
    [Total Deliveries Completed],
    0
)
```
- **Format**: Percentage (`0.0%`)

### Measure 13: Severe SLA Breaches Count (>15 Mins Delay)
```dax
[Severe SLA Breaches] = 
CALCULATE(
    COUNTROWS(Fact_Deliveries),
    Fact_Deliveries[sla_status] = "Severe Breach (>15m)"
)
```

### Measure 14: Severe Breach Rate %
```dax
[Severe Breach Rate %] = 
DIVIDE(
    [Severe SLA Breaches],
    [Total Deliveries Completed],
    0
)
```

### Measure 15: Average Delivery Duration (Minutes)
```dax
[Avg Delivery Duration (Mins)] = 
AVERAGE(Fact_Deliveries[actual_delivery_mins])
```
- **Format**: Decimal (`0.0`)

### Measure 16: Average Estimated ETA (Minutes)
```dax
[Avg Estimated ETA (Mins)] = 
AVERAGE(Fact_Deliveries[estimated_delivery_mins])
```

### Measure 17: Average Delivery Distance (KM)
```dax
[Avg Trip Distance (KM)] = 
AVERAGE(Fact_Deliveries[distance_km])
```

### Measure 18: Average Delivery Partner Rating
```dax
[Avg Delivery Rating] = 
AVERAGE(Fact_Deliveries[delivery_rating])
```
- **Format**: Decimal (`0.00`)

---

## 3. Time Intelligence & Growth Calculations

### Measure 19: Prior Month Net GMV
```dax
[Net GMV Last Month] = 
CALCULATE(
    [Net Delivered GMV],
    DATEADD(Dim_Date[Date], -1, MONTH)
)
```

### Measure 20: Month-over-Month (MoM) GMV Growth %
```dax
[MoM GMV Growth %] = 
VAR CurrentGMV = [Net Delivered GMV]
VAR PriorGMV = [Net GMV Last Month]
RETURN
    IF(
        ISBLANK(PriorGMV),
        BLANK(),
        DIVIDE(CurrentGMV - PriorGMV, PriorGMV, 0)
    )
```
- **Format**: Percentage (`+0.0%;-0.0%;0.0%`)

### Measure 21: Year-to-Date (YTD) Delivered GMV
```dax
[Net GMV YTD] = 
TOTALYTD([Net Delivered GMV], Dim_Date[Date])
```

### Measure 22: 7-Day Moving Average Revenue
```dax
[7-Day Moving Avg Revenue] = 
AVERAGEX(
    DATESINPERIOD(Dim_Date[Date], LASTDATE(Dim_Date[Date]), -7, DAY),
    [Net Delivered GMV]
)
```

---

## 4. Customer Behavioral & Cohort Measures

### Measure 23: Unique Transacting Customers
```dax
[Active Transacting Customers] = 
CALCULATE(
    DISTINCTCOUNT(Fact_Orders[customer_id]),
    Fact_Orders[order_status] = "Delivered"
)
```

### Measure 24: Average Revenue per Customer (ARPU)
```dax
[ARPU] = 
DIVIDE(
    [Net Delivered GMV],
    [Active Transacting Customers],
    0
)
```

### Measure 25: Repeat Customer Rate %
```dax
[Repeat Customer Rate %] = 
VAR CustomersWithMultipleOrders = 
    COUNTROWS(
        FILTER(
            VALUES(Fact_Orders[customer_id]),
            CALCULATE(
                COUNTROWS(Fact_Orders),
                Fact_Orders[order_status] = "Delivered"
            ) > 1
        )
    )
VAR TotalActiveCustomers = [Active Transacting Customers]
RETURN
    DIVIDE(CustomersWithMultipleOrders, TotalActiveCustomers, 0)
```

### Measure 26: Gold Members Revenue Share %
```dax
[Gold Member GMV Share %] = 
DIVIDE(
    CALCULATE([Net Delivered GMV], Dim_Customer[customer_segment] = "Gold Member"),
    [Net Delivered GMV],
    0
)
```

---

## 5. Dynamic KPI Formatting & Conditional Titles

### Measure 27: Dynamic Executive Header
```dax
[Dynamic KPI Header] = 
VAR SelectedCity = SELECTEDVALUE(Dim_Customer[city], "All Metro Cities")
VAR SelectedYear = SELECTEDVALUE(Dim_Date[Year], 2024)
RETURN
    "Food Delivery Executive Cockpit | " & SelectedCity & " (" & SelectedYear & ")"
```

### Measure 28: SLA Compliance Color Alert (Hex Code)
```dax
[SLA Alert Color Hex] = 
SWITCH(
    TRUE(),
    [SLA Compliance Rate %] >= 0.85, "#10B981", -- Green (Target achieved)
    [SLA Compliance Rate %] >= 0.75, "#F59E0B", -- Amber (Warning)
    "#EF4444"                                   -- Red (Critical Breach)
)
```
- **Usage**: Used in Power BI Conditional Formatting $\rightarrow$ **Field Value** $\rightarrow$ `[SLA Alert Color Hex]`.

### Measure 29: Lost Revenue from Cancellations
```dax
[Lost Revenue (Cancellations)] = 
CALCULATE(
    SUM(Fact_Orders[subtotal_amount]),
    Fact_Orders[order_status] = "Cancelled"
)
```

### Measure 30: Delivery Partner Fleet Efficiency Score
```dax
[Fleet Efficiency Index] = 
([SLA Compliance Rate %] * 0.60) + (([Avg Delivery Rating] / 5.0) * 0.40)
```
- **Format**: Percentage (`0.0%`)