import sqlite3
from flask import Flask, request, redirect, url_for, flash, render_template

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "secret_key"

def get_db_connection():
    conn = sqlite3.connect('reservations.db')
    conn.row_factory = sqlite3.Row
    return conn

def check_credentials(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.route("/")
def home():
    return "<h>This is the Home Page, to be improved upon</h><a href='/admin_login'>Go to Admin Login</a>"

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_credentials(username, password):
            flash("Logged in", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid login.", "error")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    return "<h1>Welcome to the Admin Dashboard!</h1>"


app.run(host="0.0.0.0")
