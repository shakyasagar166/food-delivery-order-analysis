# Excel Formulas & Analytics Guide - Food Delivery Order Analysis

This guide explains the analytical architecture, advanced formulas, pivot tables, and interview concepts applied in the `Food_Delivery_Analysis.xlsx` workbook.

---

## 1. Advanced Formulas Used in the Project

### A. Dynamic Data Lookups: `XLOOKUP` vs `VLOOKUP`
In modern analytics, `XLOOKUP` replaces legacy `VLOOKUP` and `INDEX-MATCH` because it looks both left and right, defaults to exact match, and handles `#N/A` gracefully.

```excel
=XLOOKUP(B2, Customers!A:A, Customers!E:E, "Unknown City", 0)
```
- **Explanation**: Searches for the `Customer ID` in column `B2` across the `Customers` sheet and retrieves their registered `City` from column `E:E`. If the customer is not found, it returns `"Unknown City"` instead of throwing `#N/A`.
- **Why it matters**: Zero risk of broken column indexes when columns are added or removed.

---

### B. Multi-Condition Aggregations: `SUMIFS` & `COUNTIFS`
Used on the `Executive_KPIs` tab to calculate monthly metrics from the raw transaction data.

#### Monthly Delivered Revenue:
```excel
=SUMIFS(Orders_Data!M:M, Orders_Data!E:E, ">=2024-01-01", Orders_Data!E:E, "<=2024-01-31", Orders_Data!G:G, "Delivered")
```
- **Range 1**: Sum the Net Total Amount (`Orders_Data!M:M`).
- **Condition 1 & 2**: Order date must fall between Jan 1, 2024 and Jan 31, 2024.
- **Condition 3**: Order Status must strictly match `"Delivered"`.

#### Cancellation Volume:
```excel
=COUNTIFS(Orders_Data!E:E, ">=2024-01-01", Orders_Data!E:E, "<=2024-01-31", Orders_Data!G:G, "Cancelled")
```

---

### C. Conditional Average: `AVERAGEIFS`
Calculates Average Order Value (AOV) excluding cancellations and refunds:
```excel
=AVERAGEIFS(Orders_Data!M:M, Orders_Data!E:E, ">=2024-01-01", Orders_Data!E:E, "<=2024-01-31", Orders_Data!G:G, "Delivered")
```

---

### D. Variance & Dynamic Status Flags: Nested `IFS`
Categorizes delivery latency against system ETA:
```excel
=IFS(
    Q2 <= P2 + 3, "On-Time",
    Q2 <= P2 + 15, "Minor Delay (<15m)",
    TRUE, "Severe Breach (>15m)"
)
```
- `Q2`: Actual Delivery Duration in minutes.
- `P2`: System Estimated Delivery Duration in minutes.

---

### E. Error Handling: `IFERROR`
Prevents `#DIV/0!` errors when dividing during zero-order periods:
```excel
=IFERROR((Delivered_Orders / Total_Orders) * 100, 0)
```

---

## 2. Pivot Table Design & Cross-Tabulations
The workbook features two core pivot architectures on the `Pivot_Analysis` tab:

1. **City vs Cuisine GMV Matrix**:
   - **Rows**: `City` (Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune).
   - **Columns**: `Cuisine Type` (North Indian, Biryani, Chinese, Italian, etc.).
   - **Values**: `SUM of Total Amount` formatted as Currency (`₹ #,##0`).
   - **Insight**: Highlights which regional markets generate the highest average ticket size per cuisine.

2. **Cancellation Root Cause Distribution**:
   - **Rows**: `Cancellation Reason`.
   - **Values**: `Count of Order ID`, `% of Grand Total`, and `Sum of Subtotal`.
   - **Insight**: Isolates operational failures (e.g., "Late Rider Assignment" accounting for >35% of drops) vs customer behavioral changes.

---

## 3. Cohort Retention Heatmap (Tab 5)
- Tracks user cohorts by first purchase month ($Month\ 0$).
- Tracks recurring purchases across $Month\ 1$ through $Month\ 6$.
- Uses 3-color soft conditional formatting:
  - **Green (>= 50%)**: Healthy customer stickiness.
  - **Yellow (30% - 49%)**: Moderate attrition.
  - **Red (< 30%)**: Critical drop-off requiring CRM coupon campaigns.

---

## 4. Key Business Analyst Excel Interview Questions

### Q1: What is the difference between `VLOOKUP`, `INDEX-MATCH`, and `XLOOKUP`?
> **Answer**: `VLOOKUP` only searches left-to-right, requires hardcoded column index numbers (which break when columns are inserted), and defaults to approximate match. `INDEX-MATCH` overcomes left-lookup limitations and is faster on large workbooks. `XLOOKUP` is the modern standard: bidirectional, defaults to exact match, supports native wildcard searches, and has built-in `if_not_found` error handling.

### Q2: How do you optimize an Excel sheet with 500,000 rows that is lagging?
> **Answer**:
> 1. Convert entire column references (e.g. `A:A`) to structured Excel Tables (`Table1[Amount]`) to limit calculation scope.
> 2. Avoid volatile formulas like `OFFSET()`, `INDIRECT()`, `TODAY()`, and `NOW()`.
> 3. Use Power Query (Get & Transform Data) to clean and transform raw records before loading only the aggregated summary to the sheet.
> 4. Switch Calculation Mode to "Manual" while making structural edits.

### Q3: How do you calculate Month-over-Month (MoM) Growth in Excel?
> **Answer**:
> `=(Current_Month_Revenue - Prior_Month_Revenue) / Prior_Month_Revenue` formatted as percentage. In Pivot Tables, right-click the Value field $\rightarrow$ **Show Values As** $\rightarrow$ **% Difference From** $\rightarrow$ Base Field: `Order_Month`, Base Item: `(previous)`.