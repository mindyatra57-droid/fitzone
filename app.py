print("THIS IS NEW VERSION RUNNING")
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

members = []

@app.route("/", methods=["GET", "POST"])
def index():
    global members

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        plan = request.form["plan"]

        members.append({
            "name": name,
            "age": age,
            "plan": plan
        })

        return redirect("/")

    return render_template(
        "index.html",
        members=members,
        total_members=len(members),
        active_members=len(members)
    )

    return render_template(
        "index.html",
        members=members,
        total_members=total_members,
        active_members=active_members
    )
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)