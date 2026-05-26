from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "gym_secret_key"


# DATABASE CREATE
def init_db():

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()


init_db()


# HOME
@app.route("/", methods=["GET", "POST"])
def index():

    # LOGIN PROTECTION
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    # ADD MEMBER
    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        plan = request.form["plan"]

        cursor.execute(
           """
INSERT INTO members
(name, age, plan, payment, amount)
VALUES (?, ?, ?, ?, ?)
"""
           (name, age, plan, payment, amount)
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

    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM members WHERE id = ?", (id,))

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
        cursor.execute(
            "UPDATE members SET name=?, age=?, plan=? WHERE id=?",
            (name, age, plan, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM members WHERE id=?", (id,))
    member = cursor.fetchone()

    conn.close()

    return render_template("edit.html", member=member)


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


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)