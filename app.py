from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from datetime import date

app = Flask(__name__)
app.secret_key = "gym_secret_key"


# DATABASE
def init_db():

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    # MEMBERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        plan TEXT,
        payment TEXT,
        amount TEXT
    )
    """)

    # ATTENDANCE TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_name TEXT,
        attend_date TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":

            session["admin"] = True

            return redirect("/")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")


# HOME
@app.route("/", methods=["GET", "POST"])
def index():

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    # ADD MEMBER
    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        plan = request.form["plan"]
        payment = request.form["payment"]
        amount = request.form["amount"]

        cursor.execute("""
        INSERT INTO members
        (name, age, plan, payment, amount)
        VALUES (?, ?, ?, ?, ?)
        """, (name, age, plan, payment, amount))

        conn.commit()

        return redirect("/")

    # GET MEMBERS
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    # GET ATTENDANCE
    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()

    conn.close()

    # TOTAL REVENUE
    total_revenue = 0

    for m in members:

        try:
            total_revenue += int(m[5])

        except:
            pass

    return render_template(
        "index.html",
        members=members,
        attendance=attendance,
        total_members=len(members),
        active_members=len(members),
        total_revenue=total_revenue
    )


# DELETE MEMBER
@app.route("/delete/<int:id>")
def delete(id):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM members WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# EDIT MEMBER
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        plan = request.form["plan"]
        payment = request.form["payment"]
        amount = request.form["amount"]

        cursor.execute("""
        UPDATE members
        SET name=?, age=?, plan=?, payment=?, amount=?
        WHERE id=?
        """, (name, age, plan, payment, amount, id))

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute(
        "SELECT * FROM members WHERE id=?",
        (id,)
    )

    member = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        member=member
    )


# ATTENDANCE
@app.route("/attendance/<name>")
def attendance(name):

    if "admin" not in session:
        return redirect("/login")

    today = str(date.today())

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO attendance
    (member_name, attend_date)
    VALUES (?, ?)
    """, (name, today))

    conn.commit()
    conn.close()

    return redirect("/")


# RUN APP
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)