"""
QuickBite Food Delivery Analytics - Connected Full-Stack Backend Server
Features:
1. Auto-seeds SQLite database (data/food_delivery.db) from CSVs
2. REST API endpoints for Live KPIs, Chart Data, and Metrics
3. Live SQL Query Execution Engine (runs any custom SQL query and returns rows/columns)
4. Dynamic Excel Export Engine (converts query results to .xlsx via openpyxl)
5. Static Web Server serving the frontend
"""

import os
import sys
import json
import sqlite3
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import pandas as pd
import openpyxl
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "food_delivery.db")
EXCEL_PATH = os.path.join(BASE_DIR, "excel", "Food_Delivery_Analysis.xlsx")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
PORT = 8000

# =============================================================================
# 1. DATABASE INITIALIZATION & CSV INGESTION
# =============================================================================
def init_database():
    """Initializes SQLite database and ingests CSV datasets if not already present."""
    print("Checking database status...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if orders table exists and has rows
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("SELECT COUNT(*) FROM orders")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Database already populated ({count:,} orders found).")
            conn.close()
            return

    print("Populating SQLite database from CSV datasets...")

    csv_mapping = {
        "customers": "customers.csv",
        "restaurants": "restaurants.csv",
        "riders": "riders.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
        "deliveries": "deliveries.csv",
        "payments": "payments.csv"
    }

    for table_name, csv_file in csv_mapping.items():
        file_path = os.path.join(DATA_DIR, csv_file)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f" -> Table '{table_name}': Loaded {len(df):,} records.")
        else:
            print(f" Warning: {csv_file} not found at {file_path}")

    # Create analytical indexes
    print("Creating performance indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_cust ON orders(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_rest ON orders(restaurant_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_date ON orders(order_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_status ON orders(order_status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_delv_order ON deliveries(order_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_delv_sla ON deliveries(sla_status);")

    conn.commit()
    conn.close()
    print("Database setup complete!\n")


# =============================================================================
# 2. HTTP SERVER & API REQUEST HANDLER
# =============================================================================
class FullStackAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS for local API access
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # API Router
        if path == "/api/status":
            self.handle_api_status()
        elif path == "/api/kpis":
            self.handle_api_kpis(query_params)
        elif path == "/api/charts/monthly":
            self.handle_api_monthly()
        elif path == "/api/charts/cities":
            self.handle_api_cities()
        elif path == "/api/charts/cuisines":
            self.handle_api_cuisines()
        elif path == "/api/charts/weather":
            self.handle_api_weather()
        elif path == "/api/download-excel":
            self.handle_download_excel()
        else:
            # Fall back to static files (frontend/index.html, style.css, app.js)
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/execute-sql":
            self.handle_execute_sql()
        elif path == "/api/export-sql-excel":
            self.handle_export_sql_excel()
        else:
            self.send_error(404, "Endpoint not found")

    # -------------------------------------------------------------------------
    # API ENDPOINTS IMPLEMENTATION
    # -------------------------------------------------------------------------
    def handle_api_status(self):
        """Returns database connectivity and record counts."""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            counts = {}
            for tbl in ["customers", "restaurants", "riders", "orders", "deliveries", "payments"]:
                c.execute(f"SELECT COUNT(*) FROM {tbl}")
                counts[tbl] = c.fetchone()[0]
            conn.close()

            self.send_json_response({
                "status": "connected",
                "database": "SQLite (data/food_delivery.db)",
                "excel_ready": os.path.exists(EXCEL_PATH),
                "counts": counts
            })
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, status=500)

    def handle_api_kpis(self, params):
        """Calculates live KPIs filtered by city and customer loyalty tier."""
        city = params.get("city", ["All Cities"])[0]
        tier = params.get("tier", ["All Tiers"])[0]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        where_clauses = []
        sql_params = []

        if city != "All Cities":
            where_clauses.append("c.city = ?")
            sql_params.append(city)

        if tier != "All Tiers":
            where_clauses.append("c.customer_segment = ?")
            sql_params.append(tier)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        query = f"""
            SELECT 
                COUNT(o.order_id) AS total_orders,
                SUM(CASE WHEN o.order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
                SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
                SUM(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE 0 END) AS net_gmv,
                AVG(CASE WHEN o.order_status = 'Delivered' THEN o.total_amount ELSE NULL END) AS aov,
                SUM(CASE WHEN o.order_status = 'Delivered' THEN o.discount_amount ELSE 0 END) AS total_discounts
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            {where_sql}
        """

        c.execute(query, sql_params)
        row = c.fetchone()

        tot_orders = row[0] or 0
        delv_orders = row[1] or 0
        canc_orders = row[2] or 0
        gmv = row[3] or 0.0
        aov = row[4] or 0.0
        disc = row[5] or 0.0

        # SLA On-Time %
        sla_query = f"""
            SELECT 
                COUNT(d.delivery_id) AS total_delv,
                SUM(CASE WHEN d.sla_status = 'On-Time' THEN 1 ELSE 0 END) AS ontime_delv
            FROM deliveries d
            JOIN orders o ON d.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            {where_sql}
        """
        c.execute(sla_query, sql_params)
        sla_row = c.fetchone()
        tot_delv = sla_row[0] or 0
        ontime_delv = sla_row[1] or 0
        sla_pct = (ontime_delv * 100.0 / tot_delv) if tot_delv else 0.0
        canc_pct = (canc_orders * 100.0 / tot_orders) if tot_orders else 0.0

        conn.close()

        self.send_json_response({
            "city": city,
            "tier": tier,
            "total_orders_placed": tot_orders,
            "delivered_orders": delv_orders,
            "cancelled_orders": canc_orders,
            "net_gmv": round(gmv, 2),
            "aov": round(aov, 2),
            "total_discounts": round(disc, 2),
            "sla_ontime_pct": round(sla_pct, 1),
            "cancellation_pct": round(canc_pct, 1)
        })

    def handle_api_monthly(self):
        """Returns monthly revenue and order trajectory."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT 
                strftime('%Y-%m', order_date) AS month,
                COUNT(order_id) AS orders,
                ROUND(SUM(total_amount), 2) AS gmv
            FROM orders
            WHERE order_status = 'Delivered'
            GROUP BY strftime('%Y-%m', order_date)
            ORDER BY month ASC
        """)
        rows = c.fetchall()
        conn.close()

        data = [{"month": r[0], "orders": r[1], "gmv": r[2]} for r in rows]
        self.send_json_response(data)

    def handle_api_cities(self):
        """Returns city-wise GMV share."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT 
                c.city,
                COUNT(o.order_id) AS orders,
                ROUND(SUM(o.total_amount), 2) AS gmv
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_status = 'Delivered'
            GROUP BY c.city
            ORDER BY gmv DESC
        """)
        rows = c.fetchall()
        conn.close()

        data = [{"city": r[0], "orders": r[1], "gmv": r[2]} for r in rows]
        self.send_json_response(data)

    def handle_api_cuisines(self):
        """Returns cuisine-wise GMV share."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT 
                r.cuisine_type,
                COUNT(o.order_id) AS orders,
                ROUND(SUM(o.total_amount), 2) AS gmv
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.restaurant_id
            WHERE o.order_status = 'Delivered'
            GROUP BY r.cuisine_type
            ORDER BY gmv DESC
        """)
        rows = c.fetchall()
        conn.close()

        data = [{"cuisine": r[0], "orders": r[1], "gmv": r[2]} for r in rows]
        self.send_json_response(data)

    def handle_api_weather(self):
        """Returns weather condition vs SLA On-Time %."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT 
                weather_condition,
                COUNT(delivery_id) AS total_trips,
                ROUND(AVG(actual_delivery_mins), 1) AS avg_duration,
                ROUND(SUM(CASE WHEN sla_status = 'On-Time' THEN 1 ELSE 0 END) * 100.0 / COUNT(delivery_id), 1) AS ontime_pct
            FROM deliveries
            GROUP BY weather_condition
            ORDER BY ontime_pct DESC
        """)
        rows = c.fetchall()
        conn.close()

        data = [{"weather": r[0], "trips": r[1], "avg_duration": r[2], "ontime_pct": r[3]} for r in rows]
        self.send_json_response(data)

    def handle_execute_sql(self):
        """Executes custom or preset SQL query against the SQLite database."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            body = json.loads(post_data)
            sql = body.get("sql", "").strip()

            if not sql:
                self.send_json_response({"success": False, "error": "SQL string is empty"}, status=400)
                return

            # Safety check: allow only read operations for security
            first_word = sql.split()[0].upper()
            if first_word not in ["SELECT", "WITH"]:
                self.send_json_response({
                    "success": False,
                    "error": "Only SELECT or WITH queries are permitted in the analytics explorer."
                }, status=400)
                return

            # Adapt MySQL date formatting functions if present for SQLite compatibility
            clean_sql = sql.replace("DATE_FORMAT(order_date, '%Y-%m')", "strftime('%Y-%m', order_date)")
            clean_sql = clean_sql.replace("DATEDIFF('2024-12-31', MAX(o.order_date))", "(julianday('2024-12-31') - julianday(MAX(o.order_date)))")
            clean_sql = clean_sql.replace("DATEDIFF('2024-12-31', MAX(order_date))", "(julianday('2024-12-31') - julianday(MAX(order_date)))")
            clean_sql = clean_sql.replace("HOUR(order_time)", "cast(strftime('%H', order_time) as integer)")

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(clean_sql)
            
            columns = [desc[0] for desc in c.description] if c.description else []
            rows = c.fetchmany(100) # Cap at 100 rows for fast preview
            conn.close()

            # Format rows as dicts
            formatted_rows = []
            for r in rows:
                formatted_rows.append({columns[i]: (round(r[i], 2) if isinstance(r[i], float) else r[i]) for i in range(len(columns))})

            self.send_json_response({
                "success": True,
                "columns": columns,
                "rows": formatted_rows,
                "row_count": len(rows)
            })

        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, status=400)

    def handle_download_excel(self):
        """Streams the pre-generated Food_Delivery_Analysis.xlsx workbook."""
        if os.path.exists(EXCEL_PATH):
            with open(EXCEL_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition", 'attachment; filename="Food_Delivery_Analysis.xlsx"')
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "Excel workbook not found.")

    def handle_export_sql_excel(self):
        """Runs the query and exports result directly as a downloadable Excel workbook."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            body = json.loads(post_data)
            sql = body.get("sql", "").strip()

            clean_sql = sql.replace("DATE_FORMAT(order_date, '%Y-%m')", "strftime('%Y-%m', order_date)")
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query(clean_sql, conn)
            conn.close()

            # Create Excel in-memory using openpyxl
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Query_Results")

            excel_data = output.getvalue()

            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition", 'attachment; filename="Query_Export.xlsx"')
            self.send_header("Content-Length", str(len(excel_data)))
            self.end_headers()
            self.wfile.write(excel_data)

        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, status=400)

    def send_json_response(self, data, status=200):
        json_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(json_bytes)))
        self.end_headers()
        self.wfile.write(json_bytes)


# =============================================================================
# 3. SERVER ENTRYPOINT
# =============================================================================
if __name__ == "__main__":
    init_database()
    
    server_address = ("", PORT)
    httpd = ThreadingHTTPServer(server_address, FullStackAPIHandler)
    
    print("=" * 65)
    print("🍔 QUICKBITE FOOD DELIVERY ANALYTICS - FULL STACK SERVER")
    print(f"👉 Local Web App & API: http://localhost:{PORT}")
    print(f"👉 Serving Frontend:    {FRONTEND_DIR}")
    print(f"👉 Live Database:       {DB_PATH}")
    print(f"👉 Excel Workbook:      {EXCEL_PATH}")
    print("=" * 65)
    print("Press Ctrl+C to stop the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
        print("Server stopped cleanly.")
