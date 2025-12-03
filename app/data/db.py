import sqlite3
from pathlib import Path

# sets up the data folder and database file path
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# creates the DATA folder if it doesn't already exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# opens a connection to the database file
def connect_database(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    return conn


test_conn = connect_database()
print("Database connection successful")
print(f"Database type : {type(test_conn)} ")
test_conn.close()
print("Connection closed")
