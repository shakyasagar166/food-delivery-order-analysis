# Business Analyst Interview Guide: Food Delivery Order Analysis
## 15+ Core Interview Questions & Model Answers (MySQL + Excel + Power BI)

Use this guide to master technical and situational interview discussions when showcasing this project on your resume.

---

### Question 1: "Walk me through this project from start to finish. What problem were you solving?"
> **Model Answer**:  
> *"In this project, I evaluated the commercial performance and fulfillment logistics of a food delivery platform operating across 5 Indian metro clusters (Mumbai, Bengaluru, Delhi NCR, Hyderabad, and Pune) analyzing 4,200+ orders.  
> The core business problems were an 8.1% order cancellation rate, severe SLA delivery breaches during adverse weather and dinner peak hours, and promotional discount cannibalization.  
> I structured the project into three phases:
> 1. **MySQL 8.0 Data Pipeline**: Designed a normalized 7-table schema, ingested transaction and fulfillment telemetry, and authored 21 analytical SQL queries using window functions (`LAG`, `DENSE_RANK`), CTEs, and RFM scoring.
> 2. **Microsoft Excel Financial Model**: Built an executive workbook featuring dynamic `XLOOKUP`, `SUMIFS`, multi-dimensional pivots (City vs Cuisine), and a 6-month customer cohort retention matrix.
> 3. **Power BI Reporting Suite**: Architected a Star Schema model with a dedicated Date dimension and 30+ production DAX measures (GMV, MoM Growth, On-Time SLA %, ARPU, and Churn).  
> The key actionable takeaway was discovering that 35% of cancellations were caused by late rider assignment, and rainy weather increased delivery duration by 12.4 minutes. I recommended a predictive rider pre-dispatch algorithm and dynamic weather buffer times, projected to recover ₹400K+ in annual lost value."*

---

### Question 2: "What SQL window functions did you use, and why were they necessary?"
> **Model Answer**:  
> *"I used several SQL window functions to perform calculations across partitioned row sets without collapsing rows:
> 1. `LAG()`: Used to calculate Month-over-Month (MoM) GMV growth percentage:
>    ```sql
>    (monthly_net_gmv - LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month)) * 100.0 / 
>    LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month)
>    ```
> 2. `DENSE_RANK()`: Used to rank the top 3 revenue-generating restaurants within each city (`PARTITION BY r.city ORDER BY SUM(o.total_amount) DESC`). Unlike `RANK()`, `DENSE_RANK()` avoids skipping numbers in case of tied revenue values.
> 3. `NTILE(4)`: Used to segment customers into RFM quartiles (Recency, Frequency, Monetary) on a scale of 1 to 4 to establish behavioral personas.
> 4. `SUM() OVER(PARTITION BY city ORDER BY order_date)`: Calculated running cumulative platform revenue by city over calendar days."*

---

### Question 3: "How did you conduct Customer RFM segmentation in SQL?"
> **Model Answer**:  
> *"I used a 2-stage Common Table Expression (CTE):
> - **Stage 1 (Raw Metrics)**: Aggregated each customer's Recency (`DATEDIFF('2024-12-31', MAX(order_date))`), Frequency (`COUNT(order_id)`), and Monetary value (`SUM(total_amount)`).
> - **Stage 2 (Scoring)**: Applied `NTILE(4)` to divide users into quartiles for each dimension, with 4 representing the highest score.
> - **Persona Mapping**: Combined the scores (`R + F + M`) and applied a `CASE` statement: scores $\ge 10$ became **VIP Champions**, scores $7-9$ became **Loyal Customers**, and low recency with high historical frequency flagged **At-Risk Churn Candidates** for targeted re-engagement campaigns."*

---

### Question 4: "Why did you use XLOOKUP instead of VLOOKUP in your Excel workbook?"
> **Model Answer**:  
> *"In modern analytical workbooks, `XLOOKUP` is superior to `VLOOKUP` for three reasons:
> 1. **Bidirectional Search**: `VLOOKUP` can only search left-to-right from the index column. `XLOOKUP` can look in both directions (left or right).
> 2. **Index Stability**: `VLOOKUP` relies on hardcoded column numbers (e.g., column 5), which break when new columns are inserted into the sheet. `XLOOKUP` references the explicit return array range.
> 3. **Native Error Handling**: `XLOOKUP` has a built-in `[if_not_found]` argument, removing the need to wrap formulas in `IFERROR()`."*

---

### Question 5: "What is the difference between a Star Schema and a Snowflake Schema? Which one did you choose for Power BI and why?"
> **Model Answer**:  
> *"In a **Star Schema**, fact tables connect directly to denormalized dimension tables via single-hop relationships. In a **Snowflake Schema**, dimension tables are further normalized into sub-dimensions (e.g., `Dim_Restaurant` connecting to `Dim_Cuisine` and `Dim_City`).  
> I chose a **Star Schema** for this Power BI model because:
> 1. It provides superior query performance in Power BI's in-memory VertiPaq engine due to fewer table joins.
> 2. It simplifies DAX calculations by avoiding complex multi-hop filter traversals.
> 3. It creates an intuitive drag-and-drop experience for end-users and stakeholders."*
