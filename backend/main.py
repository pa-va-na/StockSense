from fastapi import FastAPI
from fastapi import HTTPException
import psycopg2
import math
from dotenv import load_dotenv
import os
import pandas as pd
from prophet import Prophet 
from pydantic import BaseModel
import logging
logger = logging.getLogger("uvicorn.error")
load_dotenv()
conn=psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
app = FastAPI()
class RestockIn(BaseModel):
    product_id: int
    dealer_id: int
    shop_id: int
    batch_no: str
    quantity: int
    cost_price: float
    order_date: str
    delivery_date: str
    manufacture_date: str
    expiry_date: str

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/restock")
def add_restock(restock: RestockIn):
    if restock.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    if restock.cost_price <= 0:
        raise HTTPException(status_code=400, detail="Cost price must be greater than 0")
    if restock.delivery_date < restock.order_date:
        raise HTTPException(status_code=400, detail="Delivery date cannot be before order date")
    if restock.expiry_date <= restock.manufacture_date:
        raise HTTPException(status_code=400, detail="Expiry date must be after manufacture date")

    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO RESTOCK (product_id, dealer_id, shop_id, batch_no, quantity,
                                     cost_price, order_date, delivery_date,
                                     manufacture_date, expiry_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (restock.product_id, restock.dealer_id, restock.shop_id, restock.batch_no,
             restock.quantity, restock.cost_price, restock.order_date, restock.delivery_date,
             restock.manufacture_date, restock.expiry_date)
        )
        conn.commit()
        return {"message": "Restock added successfully"}
    except Exception:
        conn.rollback()
        logger.exception("add_sale failed")
        raise HTTPException(status_code=500, detail="Could not add restock")
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
LEAD_TIME_DAYS = 3

@app.get("/inventory-overview")
def get_inventory_overview():
    query = """
        SELECT
            p.product_id, p.name, p.category,
            COALESCE(r.restocked, 0) - COALESCE(s.sold, 0) AS current_stock,
            COALESCE(s.sold::float / NULLIF(s.sale_days, 0), 0) AS avg_daily_sales
        FROM PRODUCT p
        LEFT JOIN (
            SELECT product_id, SUM(quantity) AS restocked
            FROM RESTOCK GROUP BY product_id
        ) r ON r.product_id = p.product_id
        LEFT JOIN (
            SELECT si.product_id,
                   SUM(si.quantity_sold) AS sold,
                   COUNT(DISTINCT sa.sale_date) AS sale_days
            FROM SALEITEM si JOIN SALE sa ON sa.sale_id = si.sale_id
            GROUP BY si.product_id
        ) s ON s.product_id = p.product_id
    """
    df = pd.read_sql(query, conn)

    def status(row):
        if row["current_stock"] <= 0:
            return "out"
        if row["current_stock"] < row["avg_daily_sales"] * LEAD_TIME_DAYS:
            return "low"
        return "ok"

    df["status"] = df.apply(status, axis=1)
    df["avg_daily_sales"] = df["avg_daily_sales"].round(1)
    return df.to_dict(orient="records")
@app.get("/analytics/category-totals")
def category_totals():
    query = """
        SELECT p.category, SUM(si.quantity_sold) AS total_sold
        FROM SALEITEM si
        JOIN PRODUCT p ON si.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_sold DESC
    """
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")

@app.get("/analytics/product-totals")
def product_totals():
    query = """
        SELECT p.name, SUM(si.quantity_sold) AS total_sold
        FROM SALEITEM si
        JOIN PRODUCT p ON si.product_id = p.product_id
        GROUP BY p.name
        ORDER BY total_sold ASC
    """
    df = pd.read_sql(query, conn)
    return df.to_dict(orient="records")
class SaleIn(BaseModel):
    product_id: int
    quantity: int
    shop_id: int = 3

@app.post("/sale")
def add_sale(sale: SaleIn):
    if sale.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    cur = conn.cursor()
    try:
        cur.execute("SELECT selling_price FROM PRODUCT WHERE product_id = %s", (sale.product_id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")
        price = row[0]

        cur.execute(
            """SELECT COALESCE((SELECT SUM(quantity) FROM RESTOCK WHERE product_id = %s), 0)
                    - COALESCE((SELECT SUM(quantity_sold) FROM SALEITEM WHERE product_id = %s), 0)""",
            (sale.product_id, sale.product_id),
        )
        in_stock = cur.fetchone()[0]
        if sale.quantity > in_stock:
            raise HTTPException(status_code=400, detail=f"Only {in_stock} in stock")

        total = price * sale.quantity

        cur.execute(
            "INSERT INTO SALE (shop_id, sale_date, total_amount) VALUES (%s, CURRENT_DATE, %s) RETURNING sale_id",
            (sale.shop_id, total),
        )
        sale_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO SALEITEM (sale_id, product_id, quantity_sold, price_at_sale) VALUES (%s, %s, %s, %s)",
            (sale_id, sale.product_id, sale.quantity, price),
        )
        conn.commit()
        return {"message": "Sale recorded", "total": float(total)}
    except HTTPException:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        logger.exception("add_sale failed")
        raise HTTPException(status_code=500, detail="Could not record sale")