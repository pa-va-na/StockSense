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
query = """
    SELECT si.product_id, p.name, si.quantity_sold
    FROM SALEITEM si
    JOIN PRODUCT p ON si.product_id = p.product_id
"""
df = pd.read_sql(query, conn)

total_sales = df.groupby("name")["quantity_sold"].sum().sort_values()
print(total_sales)
query = """
    SELECT p.category, si.quantity_sold
    FROM SALEITEM si
    JOIN PRODUCT p ON si.product_id = p.product_id
"""
df = pd.read_sql(query, conn)

category_totals = df.groupby("category")["quantity_sold"].sum().sort_values(ascending=False)
print(category_totals)
query = """
    SELECT s.sale_date, si.quantity_sold
    FROM SALEITEM si
    JOIN SALE s ON si.sale_id = s.sale_id
    JOIN PRODUCT p ON si.product_id = p.product_id
    WHERE p.name = 'Notebook'
"""
df = pd.read_sql(query, conn)
df["sale_date"] = pd.to_datetime(df["sale_date"])
df["month"] = df["sale_date"].dt.month

monthly_avg = df.groupby("month")["quantity_sold"].mean()
print(monthly_avg)