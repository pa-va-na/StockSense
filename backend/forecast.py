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

for i in range(39, 51):
    query = f"""
        SELECT s.sale_date, si.quantity_sold
        FROM SALEITEM si
        JOIN SALE s ON si.sale_id = s.sale_id
        WHERE si.product_id = {i}
        ORDER BY s.sale_date DESC
        LIMIT 7
    """
    df = pd.read_sql(query, conn)
    moving_avg = df["quantity_sold"].mean()
    print(f"Product {i}: moving average = {moving_avg}")