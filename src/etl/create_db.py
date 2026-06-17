import sqlite3

conn = sqlite3.connect("db/nifty100.db")
print("Database created!")

conn.close()
