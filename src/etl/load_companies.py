import pandas as pd
import sqlite3

df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

conn = sqlite3.connect("db/nifty100.db")

df.to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

print("Loaded companies table successfully!")

conn.close()