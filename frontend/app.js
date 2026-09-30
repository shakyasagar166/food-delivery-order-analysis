// QuickBite Food Delivery Analytics - Connected Full Stack Frontend Controller

const API_BASE = window.location.origin.startsWith('http') ? window.location.origin : 'http://localhost:8000';
let isBackendConnected = false;

// Fallback client-side data map (used if backend server is not running)
const clientFallbackMap = {
    "All Cities": { gmv: 2342850, orders: 3730, total_placed: 4200, aov: 604.14, cancel_pct: 8.1, sla_pct: 78.4 },
    "Mumbai": { gmv: 656000, orders: 1045, total_placed: 1175, aov: 627.75, cancel_pct: 8.0, sla_pct: 79.1 },
    "Bengaluru": { gmv: 609140, orders: 970, total_placed: 1090, aov: 628.00, cancel_pct: 7.9, sla_pct: 77.8 },
    "Delhi NCR": { gmv: 515420, orders: 820, total_placed: 925, aov: 628.56, cancel_pct: 8.2, sla_pct: 78.9 },
    "Hyderabad": { gmv: 328000, orders: 520, total_placed: 590, aov: 630.77, cancel_pct: 8.3, sla_pct: 79.5 },
    "Pune": { gmv: 234290, orders: 375, total_placed: 420, aov: 624.77, cancel_pct: 8.1, sla_pct: 76.2 }
};

// 21 Preset Business Analyst Queries Catalog
const PRESET_QUERIES = [
    {
        id: 1,
        title: "Query 1: Platform High-Level Executive Summary",
        purpose: "Calculates Total Placed Orders, Delivered GMV, Net AOV, and Delivery Fulfillment %.",
        sql: `SELECT 
    COUNT(order_id) AS total_orders_placed,
    SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN total_amount ELSE 0 END), 2) AS total_delivered_gmv,
    ROUND(AVG(CASE WHEN order_status = 'Delivered' THEN total_amount ELSE NULL END), 2) AS average_order_value_aov,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN discount_amount ELSE 0 END), 2) AS total_discounts_subsidized,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 2) AS fulfillment_rate_pct
FROM orders;`
    },
    {
        id: 2,
        title: "Query 2: Order Fulfillment Funnel & Status Breakdown",
        purpose: "Quantifies drop-off rates across Delivered, Cancelled, and Refunded states.",
        sql: `SELECT 
    order_status,
    COUNT(order_id) AS total_orders,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage_share,
    ROUND(SUM(total_amount), 2) AS gross_impact_value
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;`
    },
    {
        id: 3,
        title: "Query 3: Metro City Market Penetration & AOV",
        purpose: "Evaluates sales volume, customer density, and cancellation rate by metro market.",
        sql: `SELECT 
    c.city,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE 0 END), 2) AS total_revenue,
    ROUND(AVG(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE NULL END), 2) AS city_aov,
    ROUND(SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id), 2) AS cancellation_rate_pct
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;`
    },
    {
        id: 4,
        title: "Query 4: Monthly Revenue Trend & MoM Growth % (LAG)",
        purpose: "Tracks month-over-month trajectory using SQL Window function LAG().",
        sql: `WITH MonthlyRevenue AS (
    SELECT 
        strftime('%Y-%m', order_date) AS order_month,
        COUNT(order_id) AS total_monthly_orders,
        ROUND(SUM(total_amount), 2) AS monthly_net_gmv
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    order_month,
    total_monthly_orders,
    monthly_net_gmv,
    LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month) AS previous_month_gmv,
    ROUND(
        (monthly_net_gmv - LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month)) * 100.0 / 
        LAG(monthly_net_gmv, 1) OVER (ORDER BY order_month), 
        2
    ) AS mom_growth_pct
FROM MonthlyRevenue;`
    },
    {
        id: 5,
        title: "Query 5: Top 3 Restaurants per City (DENSE_RANK)",
        purpose: "Ranks top partner outlets in each metro market by delivered net revenue.",
        sql: `WITH RankedRestaurants AS (
    SELECT 
        r.city, r.restaurant_name, r.cuisine_type,
        ROUND(SUM(o.total_amount), 2) AS gross_sales,
        DENSE_RANK() OVER (PARTITION BY r.city ORDER BY SUM(o.total_amount) DESC) AS rank_in_city
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE o.order_status = 'Delivered'
    GROUP BY r.city, r.restaurant_id, r.restaurant_name, r.cuisine_type
)
SELECT * FROM RankedRestaurants WHERE rank_in_city <= 3 ORDER BY city, rank_in_city;`
    },
    {
        id: 9,
        title: "Query 9: Weather & Congestion SLA Breach Analysis",
        purpose: "Correlates weather conditions and traffic levels with delivery delay duration.",
        sql: `SELECT 
    weather_condition,
    traffic_level,
    COUNT(delivery_id) AS trip_volume,
    ROUND(AVG(actual_delivery_mins), 1) AS avg_trip_time_mins,
    ROUND(AVG(actual_delivery_mins - estimated_delivery_mins), 1) AS avg_delay_variance_mins,
    ROUND(SUM(CASE WHEN sla_status = 'Severe Breach (>15m)' THEN 1 ELSE 0 END) * 100.0 / COUNT(delivery_id), 2) AS severe_breach_rate_pct
FROM deliveries
GROUP BY weather_condition, traffic_level
ORDER BY avg_trip_time_mins DESC;`
    },
    {
        id: 13,
        title: "Query 13: Customer RFM Segmentation Model (NTILE)",
        purpose: "Segments customers into VIP Champions, Loyalists, and Churn Risks using Recency, Frequency, and Monetary scores.",
        sql: `WITH CustomerMetrics AS (
    SELECT 
        c.customer_id, c.customer_name, c.customer_segment,
        CAST(julianday('2024-12-31') - julianday(MAX(o.order_date)) AS INT) AS recency_days,
        COUNT(o.order_id) AS order_frequency,
        ROUND(SUM(o.total_amount), 2) AS monetary_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'Delivered'
    GROUP BY c.customer_id, c.customer_name, c.customer_segment
),
RFMTiles AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(4) OVER (ORDER BY order_frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM CustomerMetrics
)
SELECT customer_id, customer_name, recency_days, order_frequency, monetary_value,
    (r_score + f_score + m_score) AS composite_rfm_score,
    CASE 
        WHEN (r_score + f_score + m_score) >= 10 THEN 'VIP Champion'
        WHEN (r_score + f_score + m_score) >= 7 THEN 'Loyal Customer'
        ELSE 'At-Risk / Churn Candidate'
    END AS rfm_persona
FROM RFMTiles ORDER BY composite_rfm_score DESC LIMIT 15;`
    },
    {
        id: 17,
        title: "Query 17: Cancellation Reasons & Lost Revenue",
        purpose: "Root cause analysis isolating financial damage caused by operational bottlenecks.",
        sql: `SELECT 
    cancellation_reason,
    COUNT(order_id) AS cancelled_orders,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM orders WHERE order_status = 'Cancelled'), 2) AS pct_of_cancellations,
    ROUND(SUM(subtotal_amount), 2) AS lost_merchandise_value
FROM orders
WHERE order_status = 'Cancelled'
GROUP BY cancellation_reason
ORDER BY cancelled_orders DESC;`
    }
];

let currentQuery = PRESET_QUERIES[0];
let charts = {};

// =============================================================================
// INITIALIZATION & CONNECTION CHECK
// =============================================================================
async function checkBackendConnection() {
    const badge = document.getElementById('backendStatusBadge');
    try {
        const res = await fetch(`${API_BASE}/api/status`);
        if (res.ok) {
            const data = await res.json();
            isBackendConnected = true;
            badge.className = 'live-badge badge-connected';
            badge.innerHTML = `🟢 Live Database Connected (${data.counts.orders.toLocaleString()} orders)`;
            console.log("Connected to Backend API & Database:", data);
        } else {
            throw new Error("API returned non-200");
        }
    } catch (err) {
        isBackendConnected = false;
        badge.className = 'live-badge badge-offline';
        badge.innerHTML = '🟡 Offline Demo (Run start_app.bat for Live DB)';
        console.warn("Backend API not reachable. Using client-side demo fallback.", err);
    }
}

// =============================================================================
// KPI FILTERING & FETCH
// =============================================================================
async function triggerFilterUpdate() {
    const city = document.getElementById('cityFilter').value;
    const tier = document.getElementById('tierFilter').value;

    if (isBackendConnected) {
        try {
            const url = `${API_BASE}/api/kpis?city=${encodeURIComponent(city)}&tier=${encodeURIComponent(tier)}`;
            const res = await fetch(url);
            const data = await res.json();

            document.getElementById('kpi-gmv').innerText = '₹ ' + data.net_gmv.toLocaleString();
            document.getElementById('kpi-orders').innerText = data.delivered_orders.toLocaleString();
            document.getElementById('kpi-orders-sub').innerText = `of ${data.total_orders_placed.toLocaleString()} orders placed`;
            document.getElementById('kpi-aov').innerText = '₹ ' + data.aov.toFixed(2);
            document.getElementById('kpi-sla').innerText = data.sla_ontime_pct.toFixed(1) + '%';
            document.getElementById('kpi-cancel').innerText = data.cancellation_pct.toFixed(1) + '%';
            return;
        } catch (e) {
            console.error("Live KPI fetch failed, using fallback:", e);
        }
    }

    // Fallback logic
    const fallback = clientFallbackMap[city] || clientFallbackMap['All Cities'];
    document.getElementById('kpi-gmv').innerText = '₹ ' + fallback.gmv.toLocaleString();
    document.getElementById('kpi-orders').innerText = fallback.orders.toLocaleString();
    document.getElementById('kpi-orders-sub').innerText = `of ${fallback.total_placed.toLocaleString()} orders placed`;
    document.getElementById('kpi-aov').innerText = '₹ ' + fallback.aov.toFixed(2);
    document.getElementById('kpi-sla').innerText = fallback.sla_pct.toFixed(1) + '%';
    document.getElementById('kpi-cancel').innerText = fallback.cancel_pct.toFixed(1) + '%';
}

// =============================================================================
// NAVIGATION & TABS
// =============================================================================
function navigate(viewId) {
    document.querySelectorAll('.content-view').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

    const target = document.getElementById('view-' + viewId);
    if (target) target.classList.add('active');
    if (event && event.currentTarget) event.currentTarget.classList.add('active');

    const titles = {
        'dashboard': ['Executive Performance Cockpit', 'Connected to Live Database (FY2024 Telemetry)'],
        'sql': ['Live SQL Query Execution Engine', 'Execute Custom Queries against SQLite/MySQL with 1-Click Excel Export'],
        'excel': ['Connected Microsoft Excel Analytical Model', 'Food_Delivery_Analysis.xlsx Architecture & Live Downloads'],
        'powerbi': ['Power BI Dimensional Model & DAX Hub', 'Star Schema & 30+ Production DAX Measures'],
        'docs': ['Business Requirements Document (BRD) & Q&A', 'Formal Documentation & Portfolio Talking Points']
    };

    if (titles[viewId]) {
        document.getElementById('page-title').innerText = titles[viewId][0];
        document.getElementById('page-subtitle').innerText = titles[viewId][1];
    }
}

function switchDoc(docId) {
    document.querySelectorAll('.doc-content').forEach(d => d.classList.remove('active'));
    document.querySelectorAll('.doc-tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('doc-' + docId).classList.add('active');
    if (event && event.currentTarget) event.currentTarget.classList.add('active');
}

// =============================================================================
// LIVE SQL EXECUTION ENGINE
// =============================================================================
function renderPresetQueryList() {
    const list = document.getElementById('queryItemsList');
    if (!list) return;

    list.innerHTML = '';
    PRESET_QUERIES.forEach((q, idx) => {
        const btn = document.createElement('button');
        btn.className = `q-btn ${idx === 0 ? 'active' : ''}`;
        btn.innerText = q.title;
        btn.onclick = () => selectPresetQuery(q, btn);
        list.appendChild(btn);
    });

    selectPresetQuery(PRESET_QUERIES[0]);
}

function selectPresetQuery(q, btnElement) {
    currentQuery = q;
    if (btnElement) {
        document.querySelectorAll('.q-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }

    document.getElementById('queryTitle').innerText = q.title;
    document.getElementById('queryPurpose').innerText = q.purpose;
    document.getElementById('sqlInput').value = q.sql;

    // Automatically run query
    runLiveSql();
}

async function runLiveSql() {
    const sql = document.getElementById('sqlInput').value.trim();
    const stats = document.getElementById('executionStats');
    const tableDiv = document.getElementById('queryResultTable');

    if (!sql) {
        alert("Please enter a SQL query.");
        return;
    }

    stats.innerText = "Status: Executing query on database...";
    tableDiv.innerHTML = '<p style="color:#38BDF8; padding: 16px;">⏳ Fetching live records from database...</p>';

    const startTime = performance.now();

    if (isBackendConnected) {
        try {
            const res = await fetch(`${API_BASE}/api/execute-sql`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: jsonStringify({ sql: sql })
            });

            const data = await res.json();
            const elapsed = Math.round(performance.now() - startTime);

            if (data.success) {
                stats.innerText = `Status: Success | ${data.row_count} rows returned in ${elapsed}ms`;
                renderSqlResultTable(data.columns, data.rows);
            } else {
                stats.innerText = `Status: Error in ${elapsed}ms`;
                tableDiv.innerHTML = `<div style="color:#EF4444; padding: 16px; background:#1C131D; border-radius:8px;">❌ SQL Error: ${data.error}</div>`;
            }
            return;
        } catch (err) {
            console.warn("Backend execution error, falling back to simulated output:", err);
        }
    }

    // Simulated offline fallback
    setTimeout(() => {
        stats.innerText = "Status: Executed (Offline Demo Mode)";
        renderSqlResultTable(["Metric", "Delivered Value", "Benchmark"], [
            { Metric: "Delivered Net GMV", "Delivered Value": "₹ 2,342,850", Benchmark: "Exceeded +6.5%" },
            { Metric: "Total Orders Fulfilled", "Delivered Value": "3,730 Orders", Benchmark: "88.8% Fulfillment" },
            { Metric: "Average Order Value (AOV)", "Delivered Value": "₹ 604.14", Benchmark: "₹ 565 Target" },
            { Metric: "On-Time Delivery SLA", "Delivered Value": "78.4%", Benchmark: "Target 85%" }
        ]);
    }, 250);
}

function renderSqlResultTable(columns, rows) {
    const tableDiv = document.getElementById('queryResultTable');
    if (!rows || rows.length === 0) {
        tableDiv.innerHTML = '<p style="color:#94A3B8; padding: 16px;">Query executed successfully. (0 rows returned)</p>';
        return;
    }

    let html = '<table class="data-table"><thead><tr>';
    columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';

    rows.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            let val = row[col];
            if (val === null || val === undefined) val = '<i style="color:#64748B">NULL</i>';
            html += `<td>${val}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    tableDiv.innerHTML = html;
}

function copyCurrentSql() {
    const sql = document.getElementById('sqlInput').value;
    navigator.clipboard.writeText(sql).then(() => {
        alert("SQL Query copied to clipboard!");
    });
}

async function exportSqlToExcel() {
    const sql = document.getElementById('sqlInput').value.trim();
    if (!sql) return;

    if (!isBackendConnected) {
        alert("Backend server is not running! Start start_app.bat to enable live Excel generation.");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/api/export-sql-excel`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: jsonStringify({ sql: sql })
        });

        if (res.ok) {
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "Query_Export.xlsx";
            document.body.appendChild(a);
            a.click();
            a.remove();
        } else {
            alert("Failed to export Excel. Make sure query is valid.");
        }
    } catch (e) {
        alert("Export error: " + e.message);
    }
}

function jsonStringify(obj) {
    return JSON.stringify(obj);
}

// =============================================================================
// CHARTS INITIALIZATION (LIVE & FALLBACK)
// =============================================================================
async function initializeCharts() {
    let monthlyData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        values: [184200, 179800, 201450, 198300, 212400, 205600, 221800, 218900, 224500, 235100, 241200, 256800]
    };

    let cityData = {
        labels: ['Mumbai (28%)', 'Bengaluru (26%)', 'Delhi NCR (22%)', 'Hyderabad (14%)', 'Pune (10%)'],
        values: [656000, 609140, 515420, 328000, 234290]
    };

    let cuisineData = {
        labels: ['Biryani', 'North Indian', 'Italian/Pizza', 'Chinese', 'Healthy', 'South Indian', 'Desserts'],
        values: [542000, 498000, 421000, 365000, 245000, 182000, 145000]
    };

    let weatherData = {
        labels: ['Clear', 'Extreme Heat', 'Foggy', 'Rainy'],
        values: [84.2, 79.5, 71.0, 61.5]
    };

    if (isBackendConnected) {
        try {
            const [mRes, cRes, cuRes, wRes] = await Promise.all([
                fetch(`${API_BASE}/api/charts/monthly`),
                fetch(`${API_BASE}/api/charts/cities`),
                fetch(`${API_BASE}/api/charts/cuisines`),
                fetch(`${API_BASE}/api/charts/weather`)
            ]);

            if (mRes.ok) {
                const mJson = await mRes.json();
                monthlyData.labels = mJson.map(d => d.month);
                monthlyData.values = mJson.map(d => d.gmv);
            }
            if (cRes.ok) {
                const cJson = await cRes.json();
                cityData.labels = cJson.map(d => d.city);
                cityData.values = cJson.map(d => d.gmv);
            }
            if (cuRes.ok) {
                const cuJson = await cuRes.json();
                cuisineData.labels = cuJson.map(d => d.cuisine);
                cuisineData.values = cuJson.map(d => d.gmv);
            }
            if (wRes.ok) {
                const wJson = await wRes.json();
                weatherData.labels = wJson.map(d => d.weather);
                weatherData.values = wJson.map(d => d.ontime_pct);
            }
        } catch (e) {
            console.warn("Chart live fetch error, using defaults:", e);
        }
    }

    // 1. Monthly Chart
    charts.monthly = new Chart(document.getElementById('monthlyChart'), {
        type: 'line',
        data: {
            labels: monthlyData.labels,
            datasets: [{
                label: 'Delivered Net GMV (₹)',
                data: monthlyData.values,
                borderColor: '#0D9488',
                backgroundColor: 'rgba(13, 148, 136, 0.15)',
                fill: true,
                tension: 0.35
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94A3B8' } },
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94A3B8' } }
            },
            plugins: { legend: { labels: { color: '#F8FAFC' } } }
        }
    });

    // 2. City Share
    charts.city = new Chart(document.getElementById('cityChart'), {
        type: 'doughnut',
        data: {
            labels: cityData.labels,
            datasets: [{
                data: cityData.values,
                backgroundColor: ['#0D9488', '#3B82F6', '#8B5CF6', '#F59E0B', '#EC4899'],
                borderColor: '#151F32',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { color: '#94A3B8', font: { size: 10 } } } }
        }
    });

    // 3. Cuisine Chart
    charts.cuisine = new Chart(document.getElementById('cuisineChart'), {
        type: 'bar',
        data: {
            labels: cuisineData.labels,
            datasets: [{
                label: 'GMV (₹)',
                data: cuisineData.values,
                backgroundColor: '#14B8A6',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94A3B8' } },
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94A3B8' } }
            },
            plugins: { legend: { display: false } }
        }
    });

    // 4. Weather SLA Chart
    charts.weather = new Chart(document.getElementById('weatherChart'), {
        type: 'bar',
        data: {
            labels: weatherData.labels,
            datasets: [{
                label: 'On-Time SLA %',
                data: weatherData.values,
                backgroundColor: ['#10B981', '#F59E0B', '#F97316', '#EF4444'],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94A3B8' } },
                x: { ticks: { color: '#94A3B8' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

// Hotkey: F5 or Ctrl+Enter in SQL textarea runs query
document.addEventListener('keydown', (e) => {
    if (e.key === 'F5' || (e.ctrlKey && e.key === 'Enter')) {
        const sqlTab = document.getElementById('view-sql');
        if (sqlTab && sqlTab.classList.contains('active')) {
            e.preventDefault();
            runLiveSql();
        }
    }
});

window.addEventListener('DOMContentLoaded', async () => {
    renderPresetQueryList();
    await checkBackendConnection();
    await initializeCharts();
});
