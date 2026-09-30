"""
Food Delivery Order Analysis - Professional Excel Dashboard Generator
Generates a multi-tab, formatted Excel workbook with KPI cards, Excel formulas,
pivots, and operational analysis using openpyxl.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
EXCEL_DIR = os.path.join(BASE_DIR, "excel")
os.makedirs(EXCEL_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(EXCEL_DIR, "Food_Delivery_Analysis.xlsx")
print(f"Creating Excel Dashboard at: {OUTPUT_FILE}")

# Load Raw Datasets
df_orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
df_customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
df_restaurants = pd.read_csv(os.path.join(DATA_DIR, "restaurants.csv"))
df_riders = pd.read_csv(os.path.join(DATA_DIR, "riders.csv"))
df_deliveries = pd.read_csv(os.path.join(DATA_DIR, "deliveries.csv"))

wb = openpyxl.Workbook()
# Remove default sheet
wb.remove(wb.active)

# Color Palette (Corporate Executive Navy & Teal)
NAVY_HEADER = "1E293B"
NAVY_SUB = "334155"
TEAL_ACCENT = "0D9488"
GOLD_ACCENT = "F59E0B"
LIGHT_BG = "F8FAFC"
CARD_BG = "F1F5F9"
BORDER_GRAY = "CBD5E1"
SUCCESS_GREEN = "10B981"
DANGER_RED = "EF4444"

thin_border = Border(
    left=Side(style='thin', color=BORDER_GRAY),
    right=Side(style='thin', color=BORDER_GRAY),
    top=Side(style='thin', color=BORDER_GRAY),
    bottom=Side(style='thin', color=BORDER_GRAY)
)
header_border = Border(
    left=Side(style='thin', color='FFFFFF'),
    right=Side(style='thin', color='FFFFFF'),
    top=Side(style='medium', color=NAVY_HEADER),
    bottom=Side(style='medium', color=NAVY_HEADER)
)

# =============================================================================
# TAB 1: EXECUTIVE DASHBOARD & KPIs
# =============================================================================
ws1 = wb.create_sheet(title="Executive_KPIs")
ws1.views.sheetView[0].showGridLines = True

# Title Banner
ws1.merge_cells("B2:J3")
title_cell = ws1["B2"]
title_cell.value = "FOOD DELIVERY PLATFORM - EXECUTIVE PERFORMANCE COCKPIT (FY2024)"
title_cell.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
title_cell.alignment = Alignment(horizontal="center", vertical="center")
title_cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")

ws1.merge_cells("B4:J4")
sub_cell = ws1["B4"]
sub_cell.value = "Zomato / Swiggy Analytics Model | Automated KPI Tracking & Executive Variance"
sub_cell.font = Font(name="Calibri", size=10, italic=True, color="64748B")
sub_cell.alignment = Alignment(horizontal="center", vertical="center")

# KPI Summary Cards Data
total_orders = len(df_orders)
delivered_orders = len(df_orders[df_orders["order_status"] == "Delivered"])
cancelled_orders = len(df_orders[df_orders["order_status"] == "Cancelled"])
total_gmv = df_orders[df_orders["order_status"] == "Delivered"]["total_amount"].sum()
aov = total_gmv / delivered_orders if delivered_orders else 0
ontime_trips = len(df_deliveries[df_deliveries["sla_status"] == "On-Time"])
ontime_pct = (ontime_trips / len(df_deliveries) * 100) if len(df_deliveries) else 0
cancel_pct = (cancelled_orders / total_orders * 100)

kpi_cards = [
    ("TOTAL ORDERS", f"{total_orders:,}", "All Channels", "B6", "C7"),
    ("DELIVERED GMV", f"₹ {total_gmv:,.2f}", f"{delivered_orders:,} Fulfilled", "D6", "E7"),
    ("AVG ORDER VALUE (AOV)", f"₹ {aov:,.2f}", "Net Ticket Size", "F6", "G7"),
    ("ON-TIME SLA RATE", f"{ontime_pct:.1f}%", f"{ontime_trips:,} Orders On-Time", "H6", "I7"),
    ("CANCELLATION RATE", f"{cancel_pct:.1f}%", f"{cancelled_orders:,} Orders Lost", "J6", "J7") # adjusted single col
]

# Write KPI Cards
card_positions = [
    ("B6", "C6", "B7", "C7", "TOTAL ORDERS", f"{total_orders:,}", "Total Platform Volume"),
    ("D6", "E6", "D7", "E7", "NET DELIVERED GMV", f"₹ {total_gmv:,.0f}", f"{delivered_orders:,} Delivered Orders"),
    ("F6", "G6", "F7", "G7", "AVG ORDER VALUE (AOV)", f"₹ {aov:.2f}", "Delivered Ticket Size"),
    ("H6", "I6", "H7", "I7", "ON-TIME SLA %", f"{ontime_pct:.1f}%", f"{ontime_trips:,} On-Time Trips"),
    ("J6", "K6", "J7", "K7", "CANCELLATION RATE", f"{cancel_pct:.1f}%", f"{cancelled_orders:,} Cancelled Orders")
]

for top_l, top_r, bot_l, bot_r, label, val, sub in card_positions:
    ws1.merge_cells(f"{top_l}:{top_r}")
    ws1.merge_cells(f"{bot_l}:{bot_r}")
    
    t_cell = ws1[top_l]
    t_cell.value = label
    t_cell.font = Font(name="Calibri", size=9, bold=True, color="64748B")
    t_cell.alignment = Alignment(horizontal="center", vertical="center")
    t_cell.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
    
    b_cell = ws1[bot_l]
    b_cell.value = val
    b_cell.font = Font(name="Calibri", size=15, bold=True, color=NAVY_HEADER)
    b_cell.alignment = Alignment(horizontal="center", vertical="center")
    b_cell.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
    
    for r in range(int(top_l[1:]), int(bot_r[1:]) + 1):
        for c in range(ord(top_l[0]) - ord('A') + 1, ord(top_r[0]) - ord('A') + 1):
            cell = ws1.cell(row=r, column=c)
            cell.border = thin_border

# Monthly Performance Table
ws1.merge_cells("B10:K10")
sec_title = ws1["B10"]
sec_title.value = "MONTHLY COMMERCIAL PERFORMANCE & FULFILLMENT BREAKDOWN"
sec_title.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
sec_title.alignment = Alignment(horizontal="left", vertical="center", indent=1)
sec_title.fill = PatternFill(start_color=NAVY_SUB, end_color=NAVY_SUB, fill_type="solid")

monthly_headers = [
    "Month", "Total Orders", "Delivered Orders", "Cancelled Orders",
    "Gross Subtotal (₹)", "Discounts (₹)", "Net Revenue (₹)",
    "AOV (₹)", "Fulfillment %", "SLA On-Time %"
]

for col_idx, h in enumerate(monthly_headers, start=2):
    cell = ws1.cell(row=11, column=col_idx, value=h)
    cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color=TEAL_ACCENT, end_color=TEAL_ACCENT, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

df_orders["order_month"] = pd.to_datetime(df_orders["order_date"]).dt.strftime("%Y-%m")
months = sorted(df_orders["order_month"].unique())

row_idx = 12
for m in months:
    m_orders = df_orders[df_orders["order_month"] == m]
    m_tot = len(m_orders)
    m_delv = len(m_orders[m_orders["order_status"] == "Delivered"])
    m_canc = len(m_orders[m_orders["order_status"] == "Cancelled"])
    m_subtot = m_orders[m_orders["order_status"] == "Delivered"]["subtotal_amount"].sum()
    m_disc = m_orders[m_orders["order_status"] == "Delivered"]["discount_amount"].sum()
    m_net = m_orders[m_orders["order_status"] == "Delivered"]["total_amount"].sum()
    m_aov = m_net / m_delv if m_delv else 0
    m_fulf_pct = (m_delv / m_tot * 100) if m_tot else 0
    
    # SLA for this month
    delv_merged = df_deliveries.merge(df_orders[["order_id", "order_month"]], on="order_id")
    m_sla = delv_merged[delv_merged["order_month"] == m]
    m_ontime = (len(m_sla[m_sla["sla_status"] == "On-Time"]) / len(m_sla) * 100) if len(m_sla) else 0
    
    vals = [
        m, m_tot, m_delv, m_canc,
        round(m_subtot, 2), round(m_disc, 2), round(m_net, 2),
        round(m_aov, 2), f"{m_fulf_pct:.1f}%", f"{m_ontime:.1f}%"
    ]
    
    for col_idx, v in enumerate(vals, start=2):
        cell = ws1.cell(row=row_idx, column=col_idx, value=v)
        cell.font = Font(name="Calibri", size=9)
        cell.border = thin_border
        if col_idx in [5, 6, 7, 8]:
            cell.number_format = '₹ #,##0.00'
            cell.alignment = Alignment(horizontal="right")
        elif col_idx in [3, 4, 9, 10, 11]:
            cell.alignment = Alignment(horizontal="center")
        else:
            cell.alignment = Alignment(horizontal="center")
            
    row_idx += 1

# Total Row
tot_cell = ws1.cell(row=row_idx, column=2, value="FY2024 TOTAL")
tot_cell.font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEADER)
tot_cell.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
tot_cell.alignment = Alignment(horizontal="center")
tot_cell.border = thin_border

ws1.cell(row=row_idx, column=3, value=f"=SUM(C12:C{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=4, value=f"=SUM(D12:D{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=5, value=f"=SUM(E12:E{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=6, value=f"=SUM(F12:F{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=7, value=f"=SUM(G12:G{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=8, value=f"=SUM(H12:H{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=9, value=f"=AVERAGE(I12:I{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=10, value=f"=AVERAGE(J12:J{row_idx-1})").border = thin_border
ws1.cell(row=row_idx, column=11, value=f"=AVERAGE(K12:K{row_idx-1})").border = thin_border

for c in range(3, 12):
    cell = ws1.cell(row=row_idx, column=c)
    cell.font = Font(name="Calibri", size=9, bold=True)
    cell.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
    if c in [6, 7, 8, 9]:
        cell.number_format = '₹ #,##0.00'
        cell.alignment = Alignment(horizontal="right")
    else:
        cell.alignment = Alignment(horizontal="center")

# =============================================================================
# TAB 2: CLEAN ORDERS DATA (Sample with Formulas)
# =============================================================================
ws2 = wb.create_sheet(title="Orders_Data")
ws2.views.sheetView[0].showGridLines = True

order_headers = [
    "Order ID", "Customer ID", "Restaurant ID", "Rider ID", "Order Date",
    "Order Time", "Order Status", "Subtotal (₹)", "Discount (₹)",
    "Delivery Fee (₹)", "Platform Fee (₹)", "Tax (₹)", "Total Amount (₹)",
    "Net Take Rate (₹)", "Delivery SLA Status"
]

for col_idx, h in enumerate(order_headers, start=1):
    cell = ws2.cell(row=1, column=col_idx, value=h)
    cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

delv_lookup = {r["order_id"]: r["sla_status"] for _, r in df_deliveries.iterrows()}

for r_idx, (_, row) in enumerate(df_orders.head(1500).iterrows(), start=2):
    oid = row["order_id"]
    sla = delv_lookup.get(oid, "Cancelled / Unfulfilled")
    
    # Net take rate formula demonstration: =H2 * 0.20 + K2 (Platform Commission + Platform Fee)
    net_take = round(row["subtotal_amount"] * 0.22 + row["platform_fee"], 2) if row["order_status"] == "Delivered" else 0.0
    
    row_data = [
        row["order_id"], row["customer_id"], row["restaurant_id"], row["rider_id"],
        row["order_date"], row["order_time"], row["order_status"],
        row["subtotal_amount"], row["discount_amount"], row["delivery_fee"],
        row["platform_fee"], row["tax_amount"], row["total_amount"],
        net_take, sla
    ]
    for c_idx, val in enumerate(row_data, start=1):
        cell = ws2.cell(row=r_idx, column=c_idx, value=val)
        cell.font = Font(name="Calibri", size=9)
        cell.border = thin_border
        if c_idx in [8, 9, 10, 11, 12, 13, 14]:
            cell.number_format = '₹ #,##0.00'
            cell.alignment = Alignment(horizontal="right")
        elif c_idx in [1, 2, 3, 4, 5, 6, 7]:
            cell.alignment = Alignment(horizontal="center")

# =============================================================================
# TAB 3: CITY VS CUISINE PIVOT ANALYSIS
# =============================================================================
ws3 = wb.create_sheet(title="Pivot_Analysis")
ws3.views.sheetView[0].showGridLines = True

# Title
ws3.merge_cells("B2:H2")
p_title = ws3["B2"]
p_title.value = "REGIONAL GMV & CUISINE CONTRIBUTION MATRIX (INR)"
p_title.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
p_title.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
p_title.alignment = Alignment(horizontal="center", vertical="center")

# Merge orders with restaurants
merged_rest = df_orders[df_orders["order_status"] == "Delivered"].merge(
    df_restaurants[["restaurant_id", "cuisine_type", "city"]], on="restaurant_id"
)

pivot_table = pd.pivot_table(
    merged_rest,
    values="total_amount",
    index="city",
    columns="cuisine_type",
    aggfunc="sum",
    fill_value=0
)

# Write headers
ws3.cell(row=4, column=2, value="Metro City").font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
ws3.cell(row=4, column=2).fill = PatternFill(start_color=NAVY_SUB, end_color=NAVY_SUB, fill_type="solid")
ws3.cell(row=4, column=2).alignment = Alignment(horizontal="center")
ws3.cell(row=4, column=2).border = thin_border

for col_idx, cuisine in enumerate(pivot_table.columns, start=3):
    cell = ws3.cell(row=4, column=col_idx, value=cuisine)
    cell.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color=TEAL_ACCENT, end_color=TEAL_ACCENT, fill_type="solid")
    cell.alignment = Alignment(horizontal="center")
    cell.border = thin_border

# Write pivot rows
cur_row = 5
for city, row_data in pivot_table.iterrows():
    c_cell = ws3.cell(row=cur_row, column=2, value=city)
    c_cell.font = Font(name="Calibri", size=9, bold=True)
    c_cell.border = thin_border
    c_cell.alignment = Alignment(horizontal="left", indent=1)
    
    for c_idx, val in enumerate(row_data, start=3):
        val_cell = ws3.cell(row=cur_row, column=c_idx, value=round(val, 2))
        val_cell.font = Font(name="Calibri", size=9)
        val_cell.number_format = '₹ #,##0'
        val_cell.border = thin_border
        val_cell.alignment = Alignment(horizontal="right")
    cur_row += 1

# Pivot City Total
ws3.cell(row=cur_row, column=2, value="Grand Total").font = Font(name="Calibri", size=10, bold=True, color=NAVY_HEADER)
ws3.cell(row=cur_row, column=2).fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
ws3.cell(row=cur_row, column=2).border = thin_border

for c_idx in range(3, 3 + len(pivot_table.columns)):
    col_let = get_column_letter(c_idx)
    t_cell = ws3.cell(row=cur_row, column=c_idx, value=f"=SUM({col_let}5:{col_let}{cur_row-1})")
    t_cell.font = Font(name="Calibri", size=9, bold=True)
    t_cell.number_format = '₹ #,##0'
    t_cell.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
    t_cell.border = thin_border
    t_cell.alignment = Alignment(horizontal="right")

# Section 2 on Pivot Tab: Cancellation Reasons Breakdown
ws3.merge_cells("B13:E13")
c_title = ws3["B13"]
c_title.value = "ORDER CANCELLATION ROOT CAUSE ANALYSIS"
c_title.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
c_title.fill = PatternFill(start_color=NAVY_SUB, end_color=NAVY_SUB, fill_type="solid")
c_title.alignment = Alignment(horizontal="left", indent=1)

canc_headers = ["Cancellation Reason", "Orders Lost", "% Share", "Lost Merchandise Value (₹)"]
for c_idx, ch in enumerate(canc_headers, start=2):
    cell = ws3.cell(row=14, column=c_idx, value=ch)
    cell.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color=TEAL_ACCENT, end_color=TEAL_ACCENT, fill_type="solid")
    cell.alignment = Alignment(horizontal="center")
    cell.border = thin_border

canc_df = df_orders[df_orders["order_status"] == "Cancelled"]
canc_summary = canc_df.groupby("cancellation_reason").agg(
    orders_lost=("order_id", "count"),
    lost_val=("subtotal_amount", "sum")
).reset_index().sort_values(by="orders_lost", ascending=False)

tot_canc = len(canc_df)
c_row = 15
for _, row in canc_summary.iterrows():
    ws3.cell(row=c_row, column=2, value=row["cancellation_reason"]).font = Font(name="Calibri", size=9)
    ws3.cell(row=c_row, column=2).border = thin_border
    
    ws3.cell(row=c_row, column=3, value=row["orders_lost"]).alignment = Alignment(horizontal="center")
    ws3.cell(row=c_row, column=3).font = Font(name="Calibri", size=9)
    ws3.cell(row=c_row, column=3).border = thin_border
    
    pct = row["orders_lost"] / tot_canc if tot_canc else 0
    ws3.cell(row=c_row, column=4, value=pct).number_format = '0.0%'
    ws3.cell(row=c_row, column=4).alignment = Alignment(horizontal="center")
    ws3.cell(row=c_row, column=4).font = Font(name="Calibri", size=9)
    ws3.cell(row=c_row, column=4).border = thin_border
    
    ws3.cell(row=c_row, column=5, value=round(row["lost_val"], 2)).number_format = '₹ #,##0.00'
    ws3.cell(row=c_row, column=5).alignment = Alignment(horizontal="right")
    ws3.cell(row=c_row, column=5).font = Font(name="Calibri", size=9)
    ws3.cell(row=c_row, column=5).border = thin_border
    c_row += 1

# =============================================================================
# TAB 4: OPERATIONS & SLA DEEP DIVE
# =============================================================================
ws4 = wb.create_sheet(title="Operations_SLA")
ws4.views.sheetView[0].showGridLines = True

ws4.merge_cells("B2:G2")
op_title = ws4["B2"]
op_title.value = "LOGISTICS FULFILLMENT & SLA COMPLIANCE AUDIT"
op_title.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
op_title.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
op_title.alignment = Alignment(horizontal="center", vertical="center")

# Weather Condition Impact Table
ws4.merge_cells("B4:G4")
w_header = ws4["B4"]
w_header.value = "Weather Condition vs Delivery Duration & SLA Breaches"
w_header.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
w_header.fill = PatternFill(start_color=NAVY_SUB, end_color=NAVY_SUB, fill_type="solid")
w_header.alignment = Alignment(horizontal="left", indent=1)

weather_cols = ["Weather Condition", "Total Deliveries", "Avg Delivery Time (mins)", "Avg Distance (km)", "On-Time SLA %", "Avg Rating"]
for idx, col in enumerate(weather_cols, start=2):
    c = ws4.cell(row=5, column=idx, value=col)
    c.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
    c.fill = PatternFill(start_color=TEAL_ACCENT, end_color=TEAL_ACCENT, fill_type="solid")
    c.alignment = Alignment(horizontal="center")
    c.border = thin_border

weather_agg = df_deliveries.groupby("weather_condition").agg(
    total_trips=("delivery_id", "count"),
    avg_mins=("actual_delivery_mins", "mean"),
    avg_dist=("distance_km", "mean"),
    ontime_count=("sla_status", lambda x: (x == "On-Time").sum()),
    avg_rating=("delivery_rating", "mean")
).reset_index()

w_row = 6
for _, row in weather_agg.iterrows():
    ontime_rate = row["ontime_count"] / row["total_trips"] if row["total_trips"] else 0
    ws4.cell(row=w_row, column=2, value=row["weather_condition"]).font = Font(name="Calibri", size=9, bold=True)
    ws4.cell(row=w_row, column=3, value=row["total_trips"]).alignment = Alignment(horizontal="center")
    ws4.cell(row=w_row, column=4, value=round(row["avg_mins"], 1)).alignment = Alignment(horizontal="center")
    ws4.cell(row=w_row, column=5, value=round(row["avg_dist"], 2)).alignment = Alignment(horizontal="center")
    ws4.cell(row=w_row, column=6, value=ontime_rate).number_format = '0.0%'
    ws4.cell(row=w_row, column=6).alignment = Alignment(horizontal="center")
    ws4.cell(row=w_row, column=7, value=round(row["avg_rating"], 2)).alignment = Alignment(horizontal="center")
    
    for c in range(2, 8):
        ws4.cell(row=w_row, column=c).border = thin_border
    w_row += 1

# =============================================================================
# TAB 5: COHORT RETENTION MATRIX
# =============================================================================
ws5 = wb.create_sheet(title="Cohort_Retention")
ws5.views.sheetView[0].showGridLines = True

ws5.merge_cells("B2:J2")
coh_title = ws5["B2"]
coh_title.value = "CUSTOMER RETENTION COHORT ANALYSIS (2024)"
coh_title.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
coh_title.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
coh_title.alignment = Alignment(horizontal="center", vertical="center")

# Cohort calculation
df_orders["order_period"] = pd.to_datetime(df_orders["order_date"]).dt.to_period("M")
cohorts = df_orders[df_orders["order_status"] == "Delivered"].groupby("customer_id")["order_period"].min().reset_index()
cohorts.rename(columns={"order_period": "cohort_group"}, inplace=True)

df_merged_cohort = df_orders[df_orders["order_status"] == "Delivered"].merge(cohorts, on="customer_id")
df_merged_cohort["period_number"] = (df_merged_cohort["order_period"] - df_merged_cohort["cohort_group"]).apply(lambda x: x.n)

cohort_pivot = df_merged_cohort.pivot_table(
    index="cohort_group",
    columns="period_number",
    values="customer_id",
    aggfunc="nunique"
)

cohort_sizes = cohort_pivot.iloc[:, 0]
cohort_retention = cohort_pivot.divide(cohort_sizes, axis=0)

cohort_headers = ["Cohort Month", "Initial Customers"] + [f"Month {col}" for col in cohort_retention.columns[1:8]]

for c_idx, ch in enumerate(cohort_headers, start=2):
    cell = ws5.cell(row=4, column=c_idx, value=ch)
    cell.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color=NAVY_SUB, end_color=NAVY_SUB, fill_type="solid")
    cell.alignment = Alignment(horizontal="center")
    cell.border = thin_border

coh_row = 5
for cohort_idx, row in cohort_retention.iterrows():
    c_month_str = str(cohort_idx)
    init_size = cohort_sizes.loc[cohort_idx]
    
    ws5.cell(row=coh_row, column=2, value=c_month_str).font = Font(name="Calibri", size=9, bold=True)
    ws5.cell(row=coh_row, column=2).alignment = Alignment(horizontal="center")
    ws5.cell(row=coh_row, column=2).border = thin_border
    
    ws5.cell(row=coh_row, column=3, value=int(init_size)).alignment = Alignment(horizontal="center")
    ws5.cell(row=coh_row, column=3).font = Font(name="Calibri", size=9)
    ws5.cell(row=coh_row, column=3).border = thin_border
    
    for p_idx, col_num in enumerate(cohort_retention.columns[1:8], start=4):
        val = row.get(col_num)
        cell = ws5.cell(row=coh_row, column=p_idx)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center")
        cell.font = Font(name="Calibri", size=9)
        if pd.notna(val):
            cell.value = val
            cell.number_format = '0.0%'
            if val >= 0.50:
                cell.fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid") # soft green
            elif val >= 0.30:
                cell.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # soft yellow
            else:
                cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # soft red
        else:
            cell.value = "-"
            
    coh_row += 1

# Auto-adjust column widths across all sheets
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len and not cell.coordinate in sheet.merged_cells:
                max_len = len(val_str)
        sheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

wb.save(OUTPUT_FILE)
print(f"Successfully generated: {OUTPUT_FILE}")