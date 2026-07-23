import sqlite3
from pathlib import Path

# Absolute path to the project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Database location
DB_PATH = BASE_DIR / "db" / "nifty100.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn