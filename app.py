from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# DATABASE CREATE
def init_db():
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        plan TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# HOME
@app.route("/", methods=["GET", "POST"])
def index():

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    # ADD MEMBER
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        plan = request.form["plan"]

        cursor.execute(
            "INSERT INTO members (name, age, plan) VALUES (?, ?, ?)",
            (name, age, plan)
        )

        conn.commit()
        return redirect("/")

    # GET MEMBERS
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        members=members,
        total_members=len(members),
        active_members=len(members)
    )
# DELETE MEMBER
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM members WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)