# 🍔 Food Delivery Order Analysis (Zomato / Swiggy Business Analyst Portfolio Project)

[![Database: MySQL](https://img.shields.io/badge/Database-MySQL_8.0-00758F?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Analytics: Excel](https://img.shields.io/badge/Model-Microsoft_Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/en-us/microsoft-365/excel)
[![BI: Power BI](https://img.shields.io/badge/Dashboard-Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Frontend: Interactive UI](https://img.shields.io/badge/Frontend-Web_Dashboard-0D9488?style=for-the-badge&logo=html5&logoColor=white)](#-frontend-interactive-dashboard)

An end-to-end, industry-grade **Business Analyst Portfolio Project** analyzing 4,200+ food delivery transactions across 5 Indian metro clusters (Mumbai, Bengaluru, Delhi NCR, Hyderabad, and Pune). This repository models operations from platforms like **Zomato, Swiggy, and DoorDash**, addressing delivery SLA breaches, customer churn, cancellation loss, and unit take-rates.

---

## 📁 Consolidated All-in-One Folder Structure

Everything for this project is self-contained in this single directory:
`C:\Users\Asus\.gemini\antigravity\scratch\food-delivery-order-analysis\`

```
food-delivery-order-analysis/
├── frontend/                       # 🌐 Interactive Web Frontend UI
│   ├── index.html                  # Executive Dashboard & Project Explorer
│   ├── style.css                   # Modern dark-mode styling
│   └── app.js                      # Live filtering, Chart.js graphs, query runner
├── data/
│   ├── raw/                        # 7 Relational CSV Datasets (4,200+ orders)
│   │   ├── customers.csv           (500 records: segments, cities, demographics)
│   │   ├── restaurants.csv         (60 records: cuisines, ratings, commissions)
│   │   ├── riders.csv              (120 records: vehicle types, ratings, status)
│   │   ├── orders.csv              (4,200 records: orders, discounts, totals, cancellation codes)
│   │   ├── order_items.csv         (9,491 records: dishes, categories, unit prices)
│   │   ├── deliveries.csv          (3,878 records: distance, weather, traffic, SLA status)
│   │   └── payments.csv            (4,200 records: UPI, credit cards, net banking, status)
│   └── data_dictionary.md          # Granular data types, PK/FK constraints, business logic
├── sql/
│   ├── 01_schema_setup.sql         # Production MySQL DDL script with indexes
│   ├── 02_data_ingestion.sql       # Bulk ingestion via LOAD DATA LOCAL INFILE
│   ├── 03_business_queries.sql     # 21 Advanced BA Queries (Window functions, CTEs, RFM, Cohort)
│   └── 04_views_and_procedures.sql # BI Views & dynamic monthly reporting Stored Procedure
├── excel/
│   ├── Food_Delivery_Analysis.xlsx # Formatted Multi-Tab Excel Workbook
│   ├── generate_excel_dashboard.py # Openpyxl automated styling script
│   └── excel_formulas_guide.md     # Formulas guide (XLOOKUP, SUMIFS, Pivot Tables)
├── power_bi/
│   ├── data_model_star_schema.md   # Star Schema architecture & 1:* relationships
│   ├── dax_measures.md             # 30+ categorized production DAX measures
│   ├── dashboard_wireframes_and_spec.md # 3-page executive report wireframe & visual design
│   └── interactive_bi_preview.html # Live interactive browser dashboard (Chart.js)
├── docs/
│   ├── BRD_Business_Requirements_Document.md # Formal Business Requirements Document (BRD)
│   ├── Insights_and_Recommendations.md       # Root-cause analysis & executive deck
│   └── BA_Interview_Questions_and_Answers.md # 15+ real-world interview Q&A scripts
└── README.md                       # Main repository guide
```

---

## 🌐 Frontend Interactive Dashboard

A complete, lightweight, interactive frontend is included right inside the `frontend/` folder:
- **Executive Metric Cards**: Delivered GMV, Fulfillment %, AOV, SLA Compliance, Cancellation Rate.
- **Dynamic Filters**: Filter metrics and charts instantly by **Metro City** (Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune).
- **Interactive SQL Query Runner**: Explore all 21 Business Analyst SQL queries with one click, read explanations, copy SQL code, and inspect simulated output tables.
- **Excel Showcase**: Visual breakdown of the 5 sheets in `Food_Delivery_Analysis.xlsx` with formula walkthroughs.
- **Power BI DAX & Data Model**: Star schema visual hierarchy and 30+ copy-ready DAX formulas.
- **Business Docs Reader**: Read the BRD, Key Insights, and Interview Q&A directly in the browser!

### How to Open the Frontend:
Simply double-click `frontend/index.html` to open it in Chrome, Edge, Firefox, or any browser! No server or installation required.

---

## 📊 Core Business Metrics (FY2024 Performance)

| Key Performance Indicator | Metric Value | Benchmark / Target | Status |
| :--- | :--- | :--- | :--- |
| **Delivered Net GMV** | **₹ 2,342,850** | Target: ₹ 2.20M | **+6.5% Exceeded** |
| **Fulfilled Delivered Volume** | **3,730 Orders (88.8%)** | Target: > 85.0% | **Fulfilled** |
| **Average Order Value (AOV)** | **₹ 604.14** | Baseline: ₹ 565.00 | **+ ₹ 39.14 Uplift** |
| **On-Time Delivery SLA %** | **78.4%** | Target: > 85.0% | **SLA Breached** |
| **Platform Cancellation Rate** | **8.1% (340 Orders)** | Target: < 5.0% | **Critical Bottleneck** |
| **Gold Members GMV Contribution** | **41.8%** | Segment Base: 25% | **High LTV Pillar** |

---

## 💡 Strategic Recommendations for Executive Leadership

1. **Deploy Predictive Rider Pre-Dispatch**: Trigger rider assignment when kitchen prep hits 70% completion rather than waiting for finished food. Projected to reduce cancellations by **40%**, saving **₹ 82,000/year**.
2. **Dynamic Weather SLA & Rain Surge**: Auto-append a +10 to +15 minute buffer during precipitation $>5\text{ mm/hr}$ and allocate a ₹25 surge incentive to active riders to keep fleet supply intact.
3. **Regular-to-Gold Loyalty Conversion**: Target 140+ frequent regular customers with discounted annual Gold passes, projecting **+₹ 140,000** in incremental GMV.
4. **Merchant Quality Intervention**: Escalate restaurants with $<3.8$ customer rating that process high volume to prevent churn.
