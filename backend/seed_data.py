import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

products = {
    1: ("Rice (5kg)", "Grocery", "kg", "Local Supplier", 350),
    2: ("Cooking Oil (1L)", "Grocery", "litre", "Fortune", 150),
    3: ("Sugar (1kg)", "Grocery", "kg", "Local Supplier", 45),
    4: ("Toor Dal (1kg)", "Grocery", "kg", "Local Supplier", 130),
    5: ("Salt (1kg)", "Grocery", "kg", "Tata", 25),
    6: ("Soap", "Household", "piece", "Lifebuoy", 35),
    7: ("Shampoo Sachet", "Household", "piece", "Clinic Plus", 2),
    8: ("Toothpaste", "Household", "piece", "Colgate", 55),
    9: ("Detergent Powder (1kg)", "Household", "kg", "Surf Excel", 120),
    10: ("Notebook", "Stationery", "piece", "Classmate", 34),
    11: ("Pen (pack of 5)", "Stationery", "piece", "Cello", 25),
    12: ("Pencil Box", "Stationery", "piece", "Nataraj", 40),
}

item_to_product_id = {}

for item_id, (name, category, unit, manufacturer, price) in products.items():
    cur.execute(
        """INSERT INTO PRODUCT (name, category, unit, manufacturer, selling_price)
           VALUES (%s, %s, %s, %s, %s) RETURNING product_id""",
        (name, category, unit, manufacturer, price)
    )
    new_id = cur.fetchone()[0]
    item_to_product_id[item_id] = new_id

conn.commit()
print("Products inserted:", item_to_product_id)
cur.execute(
    "INSERT INTO SHOP (name, location) VALUES (%s, %s) RETURNING shop_id",
    ("StockSense Demo Shop", "Kochi")
)
shop_id = cur.fetchone()[0]
conn.commit()
print("Shop id:", shop_id)
df = pd.read_csv("data/train.csv")
df = df[df["store"] == 1]
df = df[df["item"].isin(products.keys())]

print(df.shape)
print(df.head())
grouped = df.groupby("date")

for date, day_rows in grouped:
    total_amount = 0
    for _, row in day_rows.iterrows():
        price = products[row["item"]][4]
        total_amount += price * row["sales"]

    cur.execute(
        "INSERT INTO SALE (shop_id, sale_date, total_amount) VALUES (%s, %s, %s) RETURNING sale_id",
        (shop_id, date, total_amount)
    )
    sale_id = cur.fetchone()[0]

    for _, row in day_rows.iterrows():
        product_id = item_to_product_id[row["item"]]
        price = products[row["item"]][4]
        cur.execute(
            """INSERT INTO SALEITEM (sale_id, product_id, quantity_sold, price_at_sale)
               VALUES (%s, %s, %s, %s)""",
            (sale_id, product_id, int(row["sales"]), price)
        )

conn.commit()
print("Seeding complete.")