from fastapi import FastAPI
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
conn=psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "hello"}
@app.get("/products")
def get_products():
    cur=conn.cursor()
    cur.execute("SELECT * FROM PRODUCT")
    row=cur.fetchall()
    return row