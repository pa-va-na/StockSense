import psycopg2
from dotenv import load_dotenv
import os
from prophet import Prophet
import pandas as pd

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

query = """
    SELECT s.sale_date, si.quantity_sold
    FROM SALEITEM si
    JOIN SALE s ON si.sale_id = s.sale_id
    WHERE si.product_id = 39
    ORDER BY s.sale_date ASC
"""
df = pd.read_sql(query, conn)
df = df.rename(columns={"sale_date": "ds", "quantity_sold": "y"})

# split: all but last 7 days = training, last 7 days = actual (hidden) values
train = df.iloc[:-7]
actual = df.iloc[-7:]

print(actual)
model = Prophet()
model.fit(train)

future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)
prophet_predictions = forecast[["ds", "yhat"]].tail(7)

# moving average: average of the 7 days just before the holdout period
last_7_before_holdout = train["y"].tail(7)
moving_avg_value = last_7_before_holdout.mean()

print("Actual values:")
print(actual[["ds", "y"]])

print("\nProphet predictions:")
print(prophet_predictions)

print(f"\nMoving average forecast (flat): {moving_avg_value}")