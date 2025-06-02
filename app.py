import secrets
import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # Placeholder login form
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Verify from DB here later
        session["user"] = username
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/add-vehicle", methods=["GET", "POST"])
def add_vehicle():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        vehicle_id = request.form["vehicle_id"]
        model_name = request.form["model_name"]
        manufacture_date = request.form["manufacture_date"]
        battery_capacity = request.form["battery_capacity"]
        motor_power = request.form["motor_power"]
        color = request.form["color"]
        notes = request.form["notes"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute(
                """INSERT INTO vehicles
                        (vehicle_id, model_name, manufacture_date, battery_capacity, motor_power, color, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    vehicle_id,
                    model_name,
                    manufacture_date,
                    battery_capacity,
                    motor_power,
                    color,
                    notes,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Error: Vehicle ID already exists!"
        conn.close()
        return redirect(url_for("dashboard"))

    return render_template("add_vehicle.html")


@app.route("/view-vehicle", methods=["GET", "POST"])
def view_vehicle():
    if "user" not in session:
        return redirect(url_for("login"))

    vehicle = None
    searched = False

    if request.method == "POST":
        vehicle_id = request.form["vehicle_id"]
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row  # To access columns by name
        c = conn.cursor()
        c.execute("SELECT * FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
        row = c.fetchone()
        conn.close()

        if row:
            vehicle = dict(row)
        searched = True

    return render_template("view_vehicle.html", vehicle=vehicle, searched=searched)


if __name__ == "__main__":
    app.run(debug=True)
