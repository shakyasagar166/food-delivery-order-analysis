"""
Food Delivery Order Analysis - Synthetic Relational Data Generator
Generates realistic, mathematically consistent business datasets mimicking Swiggy / Zomato / DoorDash.
Tables generated:
1. customers.csv
2. restaurants.csv
3. riders.csv
4. orders.csv
5. order_items.csv
6. deliveries.csv
7. payments.csv
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)

print(f"Generating datasets into: {DATA_DIR}")

CITIES = ["Mumbai", "Bengaluru", "Delhi NCR", "Hyderabad", "Pune"]
CITY_WEIGHTS = [0.28, 0.26, 0.22, 0.14, 0.10]

CUISINES = [
    "North Indian", "Biryani & Mughlai", "Chinese & Pan-Asian",
    "Italian & Fast Food", "South Indian", "Healthy & Salads", "Desserts & Bakery"
]

SEGMENTS = ["Gold Member", "Regular", "Occasional"]
SEGMENT_WEIGHTS = [0.25, 0.50, 0.25]

VEHICLES = ["Motorcycle", "Electric Vehicle", "Scooter"]
VEHICLE_WEIGHTS = [0.60, 0.25, 0.15]

PAYMENT_METHODS = ["UPI / GPay / PhonePe", "Credit Card", "Debit Card", "Cash on Delivery", "Digital Wallet"]
PAYMENT_WEIGHTS = [0.55, 0.20, 0.10, 0.10, 0.05]

WEATHER_CONDITIONS = ["Clear", "Rainy", "Foggy", "Extreme Heat"]
WEATHER_WEIGHTS = [0.68, 0.18, 0.08, 0.06]

TRAFFIC_LEVELS = ["Low", "Moderate", "Heavy", "Gridlock"]
TRAFFIC_WEIGHTS = [0.25, 0.40, 0.25, 0.10]

CANCELLATION_REASONS = [
    "Late Rider Assignment", "Customer Changed Mind", "Restaurant Out of Stock",
    "Address Not Reachable", "Payment Timeout", "Weather Emergency"
]
CANCEL_WEIGHTS = [0.35, 0.25, 0.15, 0.10, 0.10, 0.05]

FIRST_NAMES = [
    "Aarav", "Aditi", "Rohan", "Ananya", "Vikram", "Sneha", "Karan", "Pooja",
    "Arjun", "Neha", "Rahul", "Priya", "Aditya", "Divya", "Siddharth", "Kavya",
    "Amit", "Tanvi", "Varun", "Meera", "Gaurav", "Isha", "Naveen", "Swati",
    "Rishi", "Riya", "Rajesh", "Nidhi", "Manish", "Shreya", "Deepak", "Anjali"
]
LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Mehta", "Iyer", "Nair", "Reddy", "Rao",
    "Gupta", "Malhotra", "Kapoor", "Chopra", "Deshmukh", "Kulkarni", "Bose",
    "Chatterjee", "Singh", "Yadav", "Joshi", "Bhat", "Das", "Menon", "Jain"
]

RESTAURANT_PREFIXES = [
    "Royal", "The Spice", "Flavors of", "Urban", "Curry", "Golden", "Tandoori",
    "Bistro", "Cafe", "Grand", "Biryani", "Wok &", "Slice of", "Sweet", "Green"
]
RESTAURANT_SUFFIXES = [
    "Kitchen", "Dhaba", "Palace", "Treat", "Corner", "Boutique", "Junction",
    "Express", "Hub", "Central", "Bites", "Tales", "Craft", "House", "Spot"
]

MENU_ITEMS_BY_CUISINE = {
    "North Indian": [
        ("Butter Chicken", "Main Course", 340), ("Paneer Butter Masala", "Main Course", 290),
        ("Dal Makhani", "Main Course", 240), ("Garlic Naan (2 pcs)", "Breads & Rice", 110),
        ("Tandoori Roti (4 pcs)", "Breads & Rice", 90), ("Jeera Rice", "Breads & Rice", 160),
        ("Chicken Tikka (6 pcs)", "Appetizer", 310), ("Gulab Jamun (2 pcs)", "Dessert", 85)
    ],
    "Biryani & Mughlai": [
        ("Hyderabadi Chicken Dum Biryani", "Main Course", 330), ("Mutton Dum Biryani", "Main Course", 420),
        ("Paneer Dum Biryani", "Main Course", 270), ("Mirchi Ka Salan & Raita", "Appetizer", 70),
        ("Galouti Kebab (4 pcs)", "Appetizer", 350), ("Shahi Tukda", "Dessert", 120),
        ("Chicken Seekh Kebab", "Appetizer", 290), ("Thums Up (500ml)", "Beverage", 45)
    ],
    "Chinese & Pan-Asian": [
        ("Chicken Hakka Noodles", "Main Course", 260), ("Veg Fried Rice", "Main Course", 210),
        ("Chilli Chicken Gravy", "Main Course", 295), ("Veg Manchurian Dry", "Appetizer", 220),
        ("Dimsums / Momos (6 pcs)", "Appetizer", 190), ("Crispy Corn", "Appetizer", 180),
        ("Hot & Sour Chicken Soup", "Appetizer", 160), ("Iced Lemon Tea", "Beverage", 95)
    ],
    "Italian & Fast Food": [
        ("Farmhouse Gourmet Pizza (10 inch)", "Main Course", 420), ("BBQ Chicken Pizza (10 inch)", "Main Course", 490),
        ("Creamy White Sauce Pasta", "Main Course", 310), ("Spicy Arrabbiata Pasta", "Main Course", 280),
        ("Cheesy Garlic Bread", "Appetizer", 160), ("Peri Peri French Fries", "Appetizer", 140),
        ("Double Patty Cheeseburger", "Main Course", 220), ("Choco Lava Cake", "Dessert", 110)
    ],
    "South Indian": [
        ("Masala Dosa with Chutneys", "Main Course", 140), ("Ghee Roast Dosa", "Main Course", 170),
        ("Idli Vada Combo (2+1)", "Main Course", 120), ("Medu Vada (2 pcs)", "Appetizer", 95),
        ("Filter Coffee", "Beverage", 55), ("Bisibelebath with Papad", "Main Course", 160),
        ("Uttapam Platter", "Main Course", 180), ("Rava Kesari", "Dessert", 80)
    ],
    "Healthy & Salads": [
        ("Grilled Chicken Caesar Salad", "Main Course", 320), ("Mediterranean Quinoa Bowl", "Main Course", 290),
        ("Avocado & Feta Toast", "Main Course", 260), ("Cold Pressed Orange Juice", "Beverage", 140),
        ("Green Detox Smoothie", "Beverage", 160), ("Fruit & Nut Greek Yogurt", "Dessert", 180),
        ("Roasted Veggie Protein Bowl", "Main Course", 270), ("Kombucha Brew (300ml)", "Beverage", 150)
    ],
    "Desserts & Bakery": [
        ("Belgian Chocolate Waffle", "Dessert", 210), ("New York Cheesecake Slice", "Dessert", 260),
        ("Red Velvet Pastry", "Dessert", 160), ("Warm Fudge Brownie with Ice Cream", "Dessert", 195),
        ("Cold Coffee with Whipped Cream", "Beverage", 150), ("Almond Croissant", "Appetizer", 140),
        ("Assorted Macarons (4 pcs)", "Dessert", 240), ("Tiramisu Cup", "Dessert", 220)
    ]
}

# 1. Customers (500)
print("Creating Customers table...")
customers = []
start_date = datetime(2023, 6, 1)

for cid in range(1, 501):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    name = f"{fname} {lname}"
    city = np.random.choice(CITIES, p=CITY_WEIGHTS)
    segment = np.random.choice(SEGMENTS, p=SEGMENT_WEIGHTS)
    gender = random.choice(["Male", "Female", "Prefer Not to Say"])
    signup = start_date + timedelta(days=random.randint(0, 360))
    email = f"{fname.lower()}.{lname.lower()}{random.randint(10, 999)}@example.com"
    phone = f"+91-{random.randint(70000, 99999)}{random.randint(10000, 99999)}"
    
    customers.append({
        "customer_id": f"CUST-{cid:04d}",
        "customer_name": name,
        "email": email,
        "phone": phone,
        "city": city,
        "signup_date": signup.strftime("%Y-%m-%d"),
        "customer_segment": segment,
        "gender": gender
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)

# 2. Restaurants (60)
print("Creating Restaurants table...")
restaurants = []
used_names = set()

for rid in range(1, 61):
    city = np.random.choice(CITIES, p=CITY_WEIGHTS)
    cuisine = random.choice(CUISINES)
    while True:
        rname = f"{random.choice(RESTAURANT_PREFIXES)} {random.choice(RESTAURANT_SUFFIXES)} ({cuisine.split()[0]})"
        if rname not in used_names:
            used_names.add(rname)
            break
            
    rating = round(random.uniform(3.4, 4.9), 1)
    cost_for_two = random.choice([350, 450, 600, 800, 1100, 1400])
    is_exclusive = random.choice([1, 0, 0, 0])
    commission_rate = round(random.uniform(0.18, 0.28), 2)
    
    restaurants.append({
        "restaurant_id": f"REST-{rid:03d}",
        "restaurant_name": rname,
        "city": city,
        "cuisine_type": cuisine,
        "rating": rating,
        "cost_for_two": cost_for_two,
        "commission_rate": commission_rate,
        "is_exclusive": is_exclusive
    })

df_restaurants = pd.DataFrame(restaurants)
df_restaurants.to_csv(os.path.join(DATA_DIR, "restaurants.csv"), index=False)

# 3. Riders (120)
print("Creating Riders table...")
riders = []
for rider_id in range(1, 121):
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    city = np.random.choice(CITIES, p=CITY_WEIGHTS)
    vehicle = np.random.choice(VEHICLES, p=VEHICLE_WEIGHTS)
    rating = round(random.uniform(3.8, 5.0), 1)
    joining_date = datetime(2023, 7, 1) + timedelta(days=random.randint(0, 300))
    status = np.random.choice(["Active", "On Break", "Inactive"], p=[0.82, 0.12, 0.06])
    
    riders.append({
        "rider_id": f"RDR-{rider_id:03d}",
        "rider_name": f"{fname} {lname}",
        "city": city,
        "vehicle_type": vehicle,
        "rating": rating,
        "joining_date": joining_date.strftime("%Y-%m-%d"),
        "status": status
    })

df_riders = pd.DataFrame(riders)
df_riders.to_csv(os.path.join(DATA_DIR, "riders.csv"), index=False)

# 4. Orders, Order Items, Deliveries, Payments (4,200 Orders)
print("Creating Orders, Order Items, Deliveries, and Payments tables...")
orders = []
order_items = []
deliveries = []
payments = []

order_start_date = datetime(2024, 1, 1, 9, 0, 0)
num_days = 365
total_orders = 4200
item_counter = 1

rest_by_city = {city: df_restaurants[df_restaurants["city"] == city].to_dict("records") for city in CITIES}
rider_by_city = {city: df_riders[df_riders["city"] == city].to_dict("records") for city in CITIES}
cust_records = df_customers.to_dict("records")

for oid in range(1, total_orders + 1):
    order_id = f"ORD-{20240000 + oid}"
    
    cust = random.choice(cust_records)
    cust_id = cust["customer_id"]
    city = cust["city"]
    cust_seg = cust["customer_segment"]
    
    avail_restaurants = rest_by_city.get(city)
    if not avail_restaurants:
        avail_restaurants = df_restaurants.to_dict("records")
    rest = random.choice(avail_restaurants)
    rest_id = rest["restaurant_id"]
    cuisine = rest["cuisine_type"]
    comm_rate = rest["commission_rate"]
    
    day_offset = random.randint(0, num_days - 1)
    
    hour_pool = (
        [11]*2 + [12]*6 + [13]*8 + [14]*6 + [15]*3 + 
        [16]*2 + [17]*2 + [18]*4 + [19]*8 + [20]*10 + [21]*10 + [22]*7 + [23]*3
    )
    order_hour = random.choice(hour_pool)
    order_minute = random.randint(0, 59)
    order_second = random.randint(0, 59)
    order_time = order_start_date + timedelta(days=day_offset, hours=order_hour, minutes=order_minute, seconds=order_second)
    
    num_items = random.choices([1, 2, 3, 4], weights=[0.20, 0.45, 0.25, 0.10])[0]
    menu_pool = MENU_ITEMS_BY_CUISINE.get(cuisine, MENU_ITEMS_BY_CUISINE["North Indian"])
    chosen_items = random.sample(menu_pool, min(num_items, len(menu_pool)))
    
    subtotal = 0
    for item_name, category, price in chosen_items:
        qty = random.choices([1, 2, 3], weights=[0.75, 0.20, 0.05])[0]
        item_total = price * qty
        subtotal += item_total
        
        order_items.append({
            "order_item_id": f"ITEM-{item_counter:06d}",
            "order_id": order_id,
            "item_name": item_name,
            "category": category,
            "unit_price": price,
            "quantity": qty,
            "total_price": item_total
        })
        item_counter += 1
        
    if cust_seg == "Gold Member":
        discount = round(subtotal * random.choice([0.15, 0.20, 0.25]), 2)
        delivery_fee = 0.0
    elif cust_seg == "Regular":
        discount = round(subtotal * random.choice([0.0, 0.05, 0.10]), 2)
        delivery_fee = 35.0 if subtotal < 500 else 0.0
    else:
        discount = round(subtotal * random.choice([0.0, 0.0, 0.05]), 2)
        delivery_fee = 40.0
        
    platform_fee = 5.0
    tax_amount = round((subtotal - discount) * 0.05, 2)
    final_amount = max(0.0, round((subtotal - discount) + delivery_fee + platform_fee + tax_amount, 2))
    
    status = np.random.choice(["Delivered", "Cancelled", "Refunded"], p=[0.89, 0.08, 0.03])
    
    avail_riders = rider_by_city.get(city)
    if not avail_riders:
        avail_riders = df_riders.to_dict("records")
    rider = random.choice(avail_riders)
    rider_id = rider["rider_id"]
    
    cancel_reason = None
    if status == "Cancelled":
        cancel_reason = np.random.choice(CANCELLATION_REASONS, p=CANCEL_WEIGHTS)
        rider_id = None if cancel_reason == "Late Rider Assignment" else rider_id
    elif status == "Refunded":
        cancel_reason = "Quality Issue / Damaged Packaging"
        
    orders.append({
        "order_id": order_id,
        "customer_id": cust_id,
        "restaurant_id": rest_id,
        "rider_id": rider_id if rider_id else "UNASSIGNED",
        "order_date": order_time.strftime("%Y-%m-%d"),
        "order_time": order_time.strftime("%H:%M:%S"),
        "order_timestamp": order_time.strftime("%Y-%m-%d %H:%M:%S"),
        "order_status": status,
        "subtotal_amount": round(subtotal, 2),
        "discount_amount": round(discount, 2),
        "delivery_fee": round(delivery_fee, 2),
        "platform_fee": round(platform_fee, 2),
        "tax_amount": round(tax_amount, 2),
        "total_amount": round(final_amount, 2),
        "cancellation_reason": cancel_reason if cancel_reason else "N/A"
    })
    
    if status in ["Delivered", "Refunded"]:
        distance_km = round(random.uniform(1.2, 14.8), 2)
        weather = np.random.choice(WEATHER_CONDITIONS, p=WEATHER_WEIGHTS)
        traffic = np.random.choice(TRAFFIC_LEVELS, p=TRAFFIC_WEIGHTS)
        
        base_estimate = 15 + int(distance_km * 2.8)
        estimated_mins = base_estimate + (5 if traffic in ["Heavy", "Gridlock"] else 0)
        
        weather_penalty = 12 if weather == "Rainy" else (18 if weather == "Stormy" or weather == "Foggy" else 0)
        traffic_penalty = 15 if traffic == "Gridlock" else (8 if traffic == "Heavy" else (3 if traffic == "Moderate" else 0))
        noise = random.randint(-4, 6)
        
        actual_mins = max(18, base_estimate + weather_penalty + traffic_penalty + noise)
        
        pickup_time = order_time + timedelta(minutes=random.randint(12, 22))
        delivery_time = order_time + timedelta(minutes=actual_mins)
        
        if actual_mins <= estimated_mins + 3:
            sla_status = "On-Time"
        elif actual_mins <= estimated_mins + 15:
            sla_status = "Minor Delay (<15m)"
        else:
            sla_status = "Severe Breach (>15m)"
            
        delivery_rating = round(random.uniform(4.0, 5.0), 1) if sla_status == "On-Time" else round(random.uniform(1.5, 3.8), 1)
        
        deliveries.append({
            "delivery_id": f"DELV-{oid:05d}",
            "order_id": order_id,
            "rider_id": rider_id,
            "pickup_timestamp": pickup_time.strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_timestamp": delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
            "distance_km": distance_km,
            "estimated_delivery_mins": estimated_mins,
            "actual_delivery_mins": actual_mins,
            "sla_status": sla_status,
            "weather_condition": weather,
            "traffic_level": traffic,
            "delivery_rating": delivery_rating
        })
        
    payment_method = np.random.choice(PAYMENT_METHODS, p=PAYMENT_WEIGHTS)
    if status == "Cancelled":
        p_status = "Failed" if cancel_reason == "Payment Timeout" else "Refunded"
    elif status == "Refunded":
        p_status = "Refunded"
    else:
        p_status = "Successful"
        
    payments.append({
        "payment_id": f"PAY-{oid:05d}",
        "order_id": order_id,
        "payment_method": payment_method,
        "payment_status": p_status,
        "amount_paid": final_amount,
        "payment_timestamp": (order_time + timedelta(seconds=random.randint(10, 180))).strftime("%Y-%m-%d %H:%M:%S")
    })

print("Exporting data to CSV files...")
pd.DataFrame(orders).to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)
pd.DataFrame(order_items).to_csv(os.path.join(DATA_DIR, "order_items.csv"), index=False)
pd.DataFrame(deliveries).to_csv(os.path.join(DATA_DIR, "deliveries.csv"), index=False)
pd.DataFrame(payments).to_csv(os.path.join(DATA_DIR, "payments.csv"), index=False)

print("\n--- Summary of Generated Dataset ---")
print(f"Customers:    {len(df_customers):,} rows")
print(f"Restaurants:  {len(df_restaurants):,} rows")
print(f"Riders:       {len(df_riders):,} rows")
print(f"Orders:       {len(orders):,} rows")
print(f"Order Items:  {len(order_items):,} rows")
print(f"Deliveries:   {len(deliveries):,} rows")
print(f"Payments:     {len(payments):,} rows")
print("Dataset generation completed successfully!")