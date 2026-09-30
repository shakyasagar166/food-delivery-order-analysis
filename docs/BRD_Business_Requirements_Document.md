# Business Requirements Document (BRD)
## Project Name: Food Delivery Order Analysis & Fulfillment Optimization
**Document Version**: 1.0  
**Role**: Business Analyst (E-Commerce & Quick Commerce Domain)  
**Stakeholders**: VP of Operations, Head of Growth & Marketing, Logistics Fleet Director, Chief Commercial Officer (CCO)  

---

## 1. Executive Summary & Problem Statement
In food delivery platforms (benchmarked against Zomato, Swiggy, and DoorDash), operating profitability is dictated by three primary levers: **fulfillment SLA compliance**, **customer lifetime value (LTV)**, and **unit take-rates**.

During FY2024 operations across 5 metro clusters (Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune), platform telemetry surfaced critical operational friction:
- **Order Cancellation Rate**: Hovering between **7% and 9%**, with over **35% of cancellations caused by Late Rider Assignment**.
- **Delivery SLA Latency**: Rainstorms and evening traffic surges cause delivery delays exceeding 15 minutes past predicted ETA, damaging customer retention.
- **Discount Cannibalization**: Uncalibrated promotional subsidies on low-margin food cuisines erode net take-rates.

This project delivers an integrated analytical framework using **MySQL 8.0**, **Microsoft Excel**, and **Power BI** to provide continuous operational visibility, root-cause diagnosis, and strategic decision support.

---

## 2. Business Objectives & Key Results (OKRs)

| Strategic Goal | Primary Metric | Baseline | Target Objective | Expected Annual Financial Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Reduce Order Leakage** | Order Cancellation Rate % | 8.0% | **< 4.5%** | Recovers ~₹ 1.2M in annual lost merchandise value |
| **Improve SLA Fulfillment** | On-Time Delivery SLA % | 78.5% | **> 88.0%** | Reduces negative customer ratings and churn |
| **Optimize Unit Economics** | Net Platform Take-Rate | 18.2% | **> 21.5%** | Balances customer subsidies with merchant commission |
| **Fleet Productivity** | Average Order-to-Doorstep Time | 33.4 Mins | **< 28.0 Mins** | Increases trips per rider shift by 18% |

---

## 3. Project Scope & Architecture

### In-Scope
1. **Relational Database Design**: 7 normalized entities: Customers, Restaurants, Riders, Orders, Order Items, Deliveries, and Payments.
2. **SQL Analytics Engine**: 21 production-grade queries addressing executive KPIs, window-function based growth rates, customer RFM segmentation, and SLA breach audits.
3. **Excel Operational Model**: Automated multi-tab workbook featuring KPI cards, dynamic lookups (`XLOOKUP`), conditional logic, pivot tables, and customer cohort retention grids.
4. **Power BI Reporting Suite**: Star Schema data model, dedicated DAX measures table (30+ measures), dynamic slicers, and an interactive executive cockpit.
5. **Interactive Web Frontend**: Clean, responsive browser-based dashboard to visualize charts, run SQL queries, and inspect business metrics.
6. **Strategic Recommendations**: Prescriptive operational frameworks for weather-based dynamic pricing, automated fleet dispatch, and loyalty tier realignment.

### Out-of-Scope
- Real-time IoT GPS telemetry streaming from rider smartphones (data analyzed at discrete milestones: order placed, kitchen pickup, doorstep arrival).
- Direct integration with third-party payment gateway webhooks.
- Machine learning routing engine changes (focus is on descriptive and diagnostic analytics).

---

## 4. Stakeholder Matrix & Requirements

| Stakeholder Role | Primary Business Concerns | Analytical Deliverable Required |
| :--- | :--- | :--- |
| **Chief Commercial Officer (CCO)** | Net GMV, Average Order Value (AOV), city market share, cuisine profitability | Executive Overview Dashboard, MoM Growth calculations |
| **Logistics Fleet Director** | Rider idle time, weather delay bottlenecks, distance-to-delivery ratios | Operational SLA audit, Delivery time variance heatmap |
| **Head of Growth & Marketing** | Customer churn, Gold membership ROI, discount subsidy cannibalization | RFM Segmentation, Cohort retention analysis |
| **Restaurant Partner Lead** | Merchant ratings, high-volume / low-rating quality risks, commission leakage | Restaurant performance matrix, Dish popularity audit |

---

## 5. Functional Requirements (FR)

- **FR-1 [Data Integration]**: Ingest transaction logs, rider telematics, and restaurant catalog records into a standardized relational schema without foreign key constraint violations.
- **FR-2 [Executive Cockpit]**: Provide immediate at-a-glance KPI cards summarizing Gross Merchandise Value (GMV), Delivered Volume, Cancellation Rate, and AOV.
- **FR-3 [Drill-Down Capabilities]**: Enable stakeholders to slice all performance metrics by City, Customer Loyalty Tier (Gold vs Regular vs Occasional), and Calendar Month.
- **FR-4 [SLA Breach Telemetry]**: Automatically classify fulfillment duration into On-Time, Minor Delay (<15 mins), and Severe Breach (>15 mins) relative to initial predicted ETA.
- **FR-5 [Customer Persona Classification]**: Classify customers into RFM score buckets (Champions, Loyalists, At-Risk, Inactive) based on recency and spending frequency.

---

## 6. Non-Functional Requirements (NFR)

- **NFR-1 [Performance]**: Power BI report visuals and web dashboard must refresh and render under 2.5 seconds.
- **NFR-2 [Data Integrity]**: Financial totals across MySQL queries, Excel workbooks, and Power BI DAX calculations must reconcile with 100% mathematical consistency.
- **NFR-3 [Maintainability]**: All DAX measures and SQL scripts must include clear inline documentation and adhere to standard formatting conventions.
