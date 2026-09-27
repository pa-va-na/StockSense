from fastapi import FastAPI
import psycopg2
import math
from dotenv import load_dotenv
import os
import pandas as pd
from prophet import Prophet 
load_dotenv()
conn=psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "hello"}
@app.get("/products")
def get_products():
    cur=conn.cursor()
    cur.execute("SELECT * FROM PRODUCT")
    row=cur.fetchall()
    return row
def calculate_reorder_point(avg_daily_sales,max_daily_sales,lead_time):
    safety_stock = (max_daily_sales - avg_daily_sales) * lead_time
    reorder_point = (avg_daily_sales * lead_time) + safety_stock
    return reorder_point
@app.get("/reorder-point")
def get_reorder_point(avg_daily_sales: float, max_daily_sales: float, lead_time: int):
    result = calculate_reorder_point(avg_daily_sales, max_daily_sales, lead_time)
    return {"reorder_point": result}
def calculate_eoq(annual_demand, ordering_cost, holding_cost):
    eoq=math.sqrt((2*annual_demand*ordering_cost)/holding_cost)
    return eoq
@app.get("/eoq")
def get_eoq(annual_demand: float, ordering_cost: float, holding_cost: float):
    result = calculate_eoq(annual_demand, ordering_cost, holding_cost)
    return {"eoq": result}
print(calculate_eoq(3650,50,5))
def get_forecast(product_id: int, days: int = 7):
    query = f"""
        SELECT s.sale_date, si.quantity_sold
        FROM SALEITEM si
        JOIN SALE s ON si.sale_id = s.sale_id
        WHERE si.product_id = {product_id}
        ORDER BY s.sale_date ASC
    """
    df = pd.read_sql(query, conn)
    df = df.rename(columns={"sale_date": "ds", "quantity_sold": "y"})

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(days).to_dict(orient="records")

@app.get("/forecast/{product_id}")
def forecast_endpoint(product_id: int, days: int = 7):
    return get_forecast(product_id, days)
@app.get("/inventory-overview")
def get_inventory_overview():
    query = """
        SELECT 
            p.product_id, 
            p.name, 
            p.category,
            COALESCE(SUM(r.quantity), 0) - COALESCE(SUM(si.quantity_sold), 0) AS current_stock
        FROM PRODUCT p
        LEFT JOIN RESTOCK r ON p.product_id = r.product_id
        LEFT JOIN SALEITEM si ON p.product_id = si.product_id
        GROUP BY p.product_id, p.name, p.category
    """
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")