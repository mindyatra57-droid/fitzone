import sqlite3

conn = sqlite3.connect("gym.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    plan TEXT
)
""")

conn.commit()
conn.close()

print("Database created 😎🔥")