from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("gym.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        plan TEXT,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()
    print("DB READY ✅")


# run DB init once
init_db()


# ================= HOME =================
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    members = conn.execute(
        "SELECT * FROM members WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("index.html", members=members)


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = u
            session["user_id"] = user["id"]
            session["is_admin"] = user["is_admin"] if "is_admin" in user.keys() else 0
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid login ❌")

    return render_template("login.html")


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        conn = get_db()

        existing = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (u,)
        ).fetchone()

        if existing:
            conn.close()
            return render_template("signup.html", error="User already exists ❌")

        is_admin = 1 if u == "admin" else 0

        conn.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            (u, p, is_admin)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# ================= ADD MEMBER =================
@app.route("/add_member", methods=["POST"])
def add_member():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    conn = get_db()
    conn.execute(
        "INSERT INTO members (name, age, plan, user_id) VALUES (?, ?, ?, ?)",
        (data["name"], data["age"], data["plan"], session["user_id"])
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


# ================= DELETE MEMBER =================
@app.route("/delete_member", methods=["POST"])
def delete_member():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    conn = get_db()
    conn.execute(
        "DELETE FROM members WHERE id=? AND user_id=?",
        (data["id"], session["user_id"])
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


# ================= ADMIN =================
@app.route("/admin")
def admin():
    if "user_id" not in session or session.get("is_admin") != 1:
        return "Access Denied ❌"

    conn = get_db()
    members = conn.execute("SELECT * FROM members").fetchall()
    conn.close()

    return render_template("admin.html", members=members)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ================= RUN =================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)