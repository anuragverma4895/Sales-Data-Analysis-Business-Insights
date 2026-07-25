"""
Sales Data Generator
====================
Generates a realistic sales dataset with 2,500+ orders spanning Jan 2023 - Dec 2024.
Uses real Indian cities, actual product categories, proper seasonal patterns,
and realistic profit margins.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Seed for reproducibility
np.random.seed(42)

# ──────────────────────────────────────────────
# CONFIGURATION: Real-world data mappings
# ──────────────────────────────────────────────

CITY_STATE_REGION = {
    # North
    "Delhi": ("Delhi", "North"),
    "Lucknow": ("Uttar Pradesh", "North"),
    "Jaipur": ("Rajasthan", "North"),
    "Chandigarh": ("Punjab", "North"),
    "Noida": ("Uttar Pradesh", "North"),
    "Gurugram": ("Haryana", "North"),
    # South
    "Bangalore": ("Karnataka", "South"),
    "Chennai": ("Tamil Nadu", "South"),
    "Hyderabad": ("Telangana", "South"),
    "Kochi": ("Kerala", "South"),
    "Coimbatore": ("Tamil Nadu", "South"),
    "Visakhapatnam": ("Andhra Pradesh", "South"),
    # West
    "Mumbai": ("Maharashtra", "West"),
    "Pune": ("Maharashtra", "West"),
    "Ahmedabad": ("Gujarat", "West"),
    "Surat": ("Gujarat", "West"),
    "Nagpur": ("Maharashtra", "West"),
    # East
    "Kolkata": ("West Bengal", "East"),
    "Patna": ("Bihar", "East"),
    "Bhubaneswar": ("Odisha", "East"),
    "Guwahati": ("Assam", "East"),
    "Ranchi": ("Jharkhand", "East"),
}

# City population-weighted probability (metro cities get more orders)
CITY_WEIGHTS = {
    "Mumbai": 0.12, "Delhi": 0.11, "Bangalore": 0.10, "Hyderabad": 0.08,
    "Chennai": 0.07, "Kolkata": 0.06, "Pune": 0.06, "Ahmedabad": 0.05,
    "Jaipur": 0.04, "Lucknow": 0.04, "Gurugram": 0.04, "Noida": 0.03,
    "Surat": 0.03, "Chandigarh": 0.02, "Kochi": 0.02, "Coimbatore": 0.02,
    "Nagpur": 0.02, "Visakhapatnam": 0.02, "Patna": 0.02, "Bhubaneswar": 0.02,
    "Guwahati": 0.02, "Ranchi": 0.01,
}

CATEGORIES = {
    "Electronics": {
        "sub_categories": {
            "Smartphones": {"price_range": (8999, 89999), "margin": (0.08, 0.18)},
            "Laptops": {"price_range": (25999, 149999), "margin": (0.06, 0.15)},
            "Headphones": {"price_range": (499, 24999), "margin": (0.15, 0.35)},
            "Tablets": {"price_range": (9999, 64999), "margin": (0.08, 0.16)},
            "Smartwatches": {"price_range": (1999, 34999), "margin": (0.12, 0.28)},
            "Chargers & Cables": {"price_range": (199, 2999), "margin": (0.25, 0.55)},
        },
        "weight": 0.28,
    },
    "Clothing": {
        "sub_categories": {
            "T-Shirts": {"price_range": (299, 2999), "margin": (0.25, 0.50)},
            "Jeans": {"price_range": (799, 4999), "margin": (0.20, 0.45)},
            "Formal Shirts": {"price_range": (599, 3999), "margin": (0.22, 0.48)},
            "Jackets": {"price_range": (1499, 8999), "margin": (0.18, 0.40)},
            "Ethnic Wear": {"price_range": (999, 12999), "margin": (0.20, 0.45)},
        },
        "weight": 0.22,
    },
    "Furniture": {
        "sub_categories": {
            "Office Chairs": {"price_range": (3999, 29999), "margin": (0.10, 0.25)},
            "Desks": {"price_range": (4999, 39999), "margin": (0.08, 0.22)},
            "Bookshelves": {"price_range": (2999, 19999), "margin": (0.12, 0.28)},
            "Beds": {"price_range": (9999, 59999), "margin": (0.08, 0.20)},
            "Dining Tables": {"price_range": (7999, 49999), "margin": (0.10, 0.22)},
        },
        "weight": 0.15,
    },
    "Office Supplies": {
        "sub_categories": {
            "Printers": {"price_range": (3999, 29999), "margin": (0.05, 0.15)},
            "Paper & Notebooks": {"price_range": (49, 999), "margin": (0.30, 0.60)},
            "Pens & Stationery": {"price_range": (29, 499), "margin": (0.35, 0.65)},
            "Storage & Organizers": {"price_range": (299, 4999), "margin": (0.20, 0.40)},
            "Ink & Toner": {"price_range": (499, 5999), "margin": (0.15, 0.35)},
        },
        "weight": 0.18,
    },
    "Food & Beverages": {
        "sub_categories": {
            "Snacks & Chips": {"price_range": (20, 499), "margin": (0.15, 0.35)},
            "Beverages": {"price_range": (30, 599), "margin": (0.20, 0.45)},
            "Dry Fruits & Nuts": {"price_range": (199, 2999), "margin": (0.12, 0.30)},
            "Health Supplements": {"price_range": (299, 4999), "margin": (0.18, 0.38)},
            "Tea & Coffee": {"price_range": (99, 1999), "margin": (0.20, 0.40)},
        },
        "weight": 0.17,
    },
}

PRODUCT_NAMES = {
    "Smartphones": ["Samsung Galaxy M34", "Realme Narzo 60", "OnePlus Nord CE3", "Xiaomi Redmi Note 13", "Vivo T2x", "iPhone 15", "Motorola Edge 40"],
    "Laptops": ["HP Pavilion 15", "Dell Inspiron 14", "Lenovo IdeaPad Slim 3", "ASUS VivoBook 15", "Acer Aspire 5", "MacBook Air M2"],
    "Headphones": ["boAt Rockerz 450", "JBL Tune 510BT", "Sony WH-1000XM5", "Noise Buds VS104", "OnePlus Buds Z2", "Realme Buds Air 3"],
    "Tablets": ["Samsung Galaxy Tab A8", "Lenovo Tab M10", "Realme Pad Mini", "Apple iPad 10th Gen", "OnePlus Pad Go"],
    "Smartwatches": ["Noise ColorFit Pro 4", "Fire-Boltt Phoenix", "boAt Storm Call", "Samsung Galaxy Watch 5", "Apple Watch SE"],
    "Chargers & Cables": ["Anker PowerPort", "Belkin BoostCharge", "Mi 33W SonicCharge", "Portronics Adaptor", "Amazon Basics USB-C Cable"],
    "T-Shirts": ["Allen Solly Polo", "U.S. Polo Assn. Crew", "H&M Basic Tee", "Levi's Graphic Tee", "Dennis Lingo Slim Fit"],
    "Jeans": ["Levi's 511 Slim", "Wrangler Bootcut", "Pepe Jeans Slim", "Flying Machine Tapered", "Lee Cooper Skinny"],
    "Formal Shirts": ["Van Heusen Slim Fit", "Peter England Classic", "Arrow Regular Fit", "Louis Philippe Checked", "Raymond Linen Shirt"],
    "Jackets": ["Wildcraft Windbreaker", "Fort Collins Puffer", "Red Tape Bomber", "Campus Sutra Denim", "HRX Active Jacket"],
    "Ethnic Wear": ["Manyavar Kurta Set", "FabIndia Cotton Kurta", "Soch Silk Saree", "Biba Anarkali Suit", "W Palazzo Set"],
    "Office Chairs": ["Green Soul Jupiter", "IKEA Markus", "Featherlite Optima", "Nilkamal Leatherite", "HOF Ito Mesh Chair"],
    "Desks": ["IKEA Bekant Standing Desk", "Nilkamal Aries Workstation", "Wakefit Orion Study Table", "Amazon Basics L-Shape Desk", "Featherlite Amaze"],
    "Bookshelves": ["Spacewood Engineered Wood", "DeckUp Meritus", "Amazon Basics Bookcase", "Nilkamal Freedom Mini", "IKEA Kallax Shelf"],
    "Beds": ["Wakefit Orthopaedic Bed", "Sleepyhead Original", "Pepperfry Trundle Bed", "Nilkamal Imperial Queen", "IKEA Malm King Bed"],
    "Dining Tables": ["Nilkamal Shahenshah 4-Seater", "Home Centre Montoya", "Urban Ladder Danton 6-Seater", "IKEA Ekedalen", "Godrej Interio Neo"],
    "Printers": ["HP LaserJet M1005", "Canon Pixma G3060", "Epson L3250", "Brother DCP-T420W", "HP Smart Tank 580"],
    "Paper & Notebooks": ["Classmate Notebook 200pg", "Navneet Long Book", "JK Copier A4 Paper Ream", "Luxor Exercise Book", "Sundaram A4 Ruled"],
    "Pens & Stationery": ["Cello Pinpoint Blue", "Reynolds Trimax Gel", "Parker Classic Gold", "Pilot V5 Hi-Tecpoint", "Faber-Castell Kit"],
    "Storage & Organizers": ["Amazon Basics Desk Organizer", "Cello Novelty Big Drawer", "Milton Modular Box", "Tupperware Store-All", "Nilkamal Chester 24"],
    "Ink & Toner": ["HP 802 Black Cartridge", "Canon PG-745 Black", "Epson T664 Refill Bottle", "Brother BT-D60BK", "HP 678 Tri-Color"],
    "Snacks & Chips": ["Lay's Classic Salted", "Haldiram's Aloo Bhujia", "Bingo Mad Angles", "Too Yumm Multigrain", "Kurkure Masala Munch"],
    "Beverages": ["Coca-Cola 2L", "Tropicana Mixed Fruit 1L", "Paper Boat Aamras", "Real Fruit Power Mango", "Sting Energy Drink"],
    "Dry Fruits & Nuts": ["Happilo Almonds 500g", "Nutraj Cashews 250g", "Amazon Basics Mixed Nuts", "Farmley Premium Walnuts", "True Elements Trail Mix"],
    "Health Supplements": ["MuscleBlaze Whey Protein", "Ensure Nutritional Drink", "Dabur Chyawanprash 1kg", "HealthKart Multivitamin", "Revital H Capsules"],
    "Tea & Coffee": ["Tata Gold Tea 500g", "Nescafe Classic 200g", "Brooke Bond Red Label", "Bru Instant Coffee", "Organic India Tulsi Green"],
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.52, 0.30, 0.18]

PAYMENT_MODES = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
PAYMENT_WEIGHTS = [0.35, 0.22, 0.18, 0.15, 0.10]

SHIP_MODES = ["Standard", "Express", "Same Day", "Economy"]
SHIP_WEIGHTS = [0.45, 0.30, 0.15, 0.10]

# Customer name pool (Indian names)
FIRST_NAMES = [
    "Aarav", "Aditi", "Amit", "Ananya", "Arjun", "Bhavya", "Chirag", "Deepika",
    "Dev", "Diya", "Gaurav", "Ishaan", "Kavya", "Kriti", "Manish", "Meera",
    "Nandini", "Neha", "Nikhil", "Pooja", "Priya", "Rahul", "Rishi", "Rohit",
    "Sakshi", "Sanjay", "Shreya", "Sneha", "Tanvi", "Varun", "Vikram", "Zara",
    "Aditya", "Ayesha", "Harsh", "Isha", "Kunal", "Lavanya", "Mohit", "Nisha",
    "Pankaj", "Rajesh", "Simran", "Tushar", "Uma", "Vivek", "Yash", "Ritika",
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Joshi", "Reddy",
    "Nair", "Iyer", "Chopra", "Mehta", "Banerjee", "Chatterjee", "Das", "Rao",
    "Pillai", "Menon", "Shah", "Agarwal", "Mishra", "Tiwari", "Pandey", "Yadav",
    "Bhat", "Deshmukh", "Kulkarni", "Patil", "Saxena", "Malhotra", "Kapoor", "Sinha",
]


def get_seasonal_multiplier(month):
    """Returns a seasonal sales multiplier based on Indian market patterns."""
    seasonal = {
        1: 0.85,   # Jan — post-holiday slump
        2: 0.80,   # Feb — low season
        3: 0.90,   # Mar — financial year end, corporate buying
        4: 0.75,   # Apr — new financial year start, slow
        5: 0.78,   # May — summer, moderate
        6: 0.72,   # Jun — monsoon onset, dip
        7: 0.70,   # Jul — monsoon, lowest
        8: 0.82,   # Aug — Independence Day sales
        9: 0.95,   # Sep — festive season starts
        10: 1.35,  # Oct — Diwali, Dussehra (peak)
        11: 1.25,  # Nov — post-Diwali, Black Friday
        12: 1.10,  # Dec — Christmas, year-end sales
    }
    return seasonal.get(month, 1.0)


def generate_order_date(start_date, end_date):
    """Generate a single order date weighted by seasonal patterns."""
    # Generate candidate dates with seasonal weighting
    total_days = (end_date - start_date).days
    day_offset = np.random.randint(0, total_days)
    candidate = start_date + timedelta(days=day_offset)

    # Apply seasonal acceptance probability
    multiplier = get_seasonal_multiplier(candidate.month)
    if np.random.random() < multiplier / 1.35:  # Normalize by max multiplier
        return candidate
    else:
        # Retry with a new date
        return generate_order_date(start_date, end_date)


def generate_sales_data(n_orders=2500):
    """Generate the complete sales dataset."""
    print("Generating realistic sales data...")

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)

    cities = list(CITY_WEIGHTS.keys())
    city_probs = list(CITY_WEIGHTS.values())

    # Generate unique customers (roughly 600 unique customers)
    n_customers = 600
    customers = []
    for i in range(n_customers):
        fname = np.random.choice(FIRST_NAMES)
        lname = np.random.choice(LAST_NAMES)
        customers.append({
            "id": f"CUST-{1000 + i}",
            "name": f"{fname} {lname}",
            "segment": np.random.choice(SEGMENTS, p=SEGMENT_WEIGHTS),
            "city": np.random.choice(cities, p=city_probs),
        })

    records = []
    category_names = list(CATEGORIES.keys())
    category_weights = [CATEGORIES[c]["weight"] for c in category_names]

    for i in range(n_orders):
        # Order metadata
        order_date = generate_order_date(start_date, end_date)
        order_id = f"ORD-{10000 + i}"

        # Customer
        customer = np.random.choice(customers)
        city = customer["city"]
        state, region = CITY_STATE_REGION[city]

        # Product selection
        category = np.random.choice(category_names, p=category_weights)
        sub_cats = list(CATEGORIES[category]["sub_categories"].keys())
        sub_category = np.random.choice(sub_cats)
        sub_config = CATEGORIES[category]["sub_categories"][sub_category]

        # Product name
        product_name = np.random.choice(PRODUCT_NAMES[sub_category])

        # Pricing
        price_low, price_high = sub_config["price_range"]
        # Log-normal distribution for more realistic price distribution
        log_mean = (np.log(price_low) + np.log(price_high)) / 2
        log_std = (np.log(price_high) - np.log(price_low)) / 4
        unit_price = np.clip(
            np.exp(np.random.normal(log_mean, log_std)),
            price_low, price_high
        )
        unit_price = round(unit_price, 2)

        # Quantity (most orders are 1-3 items, some larger)
        if category in ["Office Supplies", "Food & Beverages"]:
            quantity = np.random.choice([1, 2, 3, 4, 5, 6, 8, 10, 12], p=[0.15, 0.20, 0.20, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03])
        elif category == "Furniture":
            quantity = np.random.choice([1, 2, 3], p=[0.70, 0.22, 0.08])
        else:
            quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.40, 0.28, 0.18, 0.09, 0.05])

        # Discount (seasonal and segment-based)
        base_discount = np.random.choice(
            [0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
            p=[0.30, 0.20, 0.18, 0.12, 0.10, 0.06, 0.04]
        )
        # Higher discounts during festive season
        if order_date.month in [10, 11]:
            base_discount = min(base_discount + 0.05, 0.35)
        # Corporate gets slightly higher discounts
        if customer["segment"] == "Corporate":
            base_discount = min(base_discount + 0.03, 0.35)
        discount = round(base_discount, 2)

        # Revenue and profit
        revenue = round(unit_price * quantity * (1 - discount), 2)

        margin_low, margin_high = sub_config["margin"]
        # High discounts eat into margin
        effective_margin = np.random.uniform(margin_low, margin_high) - (discount * 0.3)
        # Some orders can be at a loss (realistic)
        if discount >= 0.25:
            effective_margin = max(effective_margin, -0.05)
        else:
            effective_margin = max(effective_margin, 0.01)
        profit = round(revenue * effective_margin, 2)

        # Payment and shipping
        payment_mode = np.random.choice(PAYMENT_MODES, p=PAYMENT_WEIGHTS)
        ship_mode = np.random.choice(SHIP_MODES, p=SHIP_WEIGHTS)

        records.append({
            "Order_ID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Customer_ID": customer["id"],
            "Customer_Name": customer["name"],
            "Segment": customer["segment"],
            "City": city,
            "State": state,
            "Region": region,
            "Category": category,
            "Sub_Category": sub_category,
            "Product_Name": product_name,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Discount": discount,
            "Revenue": revenue,
            "Profit": profit,
            "Payment_Mode": payment_mode,
            "Ship_Mode": ship_mode,
        })

    df = pd.DataFrame(records)
    df = df.sort_values("Order_Date").reset_index(drop=True)

    # Save
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "sales_data.csv")
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} orders successfully!")
    print(f"Date range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
    print(f"Total Revenue: INR {df['Revenue'].sum():,.2f}")
    print(f"Total Profit: INR {df['Profit'].sum():,.2f}")
    print(f"Unique Customers: {df['Customer_ID'].nunique()}")
    print(f"Saved to: {output_path}")

    return df


if __name__ == "__main__":
    df = generate_sales_data(2500)
    print("\nSample Data:")
    print(df.head(10).to_string())
    print(f"\nColumn Types:\n{df.dtypes}")
    print(f"\nCategory Distribution:\n{df['Category'].value_counts()}")
    print(f"\nRegion Distribution:\n{df['Region'].value_counts()}")
