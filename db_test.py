import sqlite3

conn = sqlite3.connect("gym.db")
cursor = conn.cursor()

# 🔥 INSERT DATA
cursor.execute("INSERT INTO members (name, age, plan) VALUES (?, ?, ?)", ("Aman", 20, "Basic"))
cursor.execute("INSERT INTO members (name, age, plan) VALUES (?, ?, ?)", ("Rahul", 25, "Premium"))

conn.commit()

# 📊 SHOW DATA
cursor.execute("SELECT * FROM members")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()