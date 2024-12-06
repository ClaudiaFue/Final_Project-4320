import sqlite3
from flask import Flask, request, redirect, url_for, flash, render_template
import random
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
    return render_template("home.html")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_credentials(username, password):
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    seating_chart = [['0' for _ in range(4)] for _ in range(12)]
    cursor.execute("SELECT seatRow, seatColumn FROM reservations")
    reserved = cursor.fetchall()
    for seat in reserved:
        row, col = seat
        seating_chart[row-1][col-1] = 'X'
    cursor.execute("SELECT SUM(price) FROM reservations")
    result = cursor.fetchone()
    sales = result[0] if result[0] is not None else 0

    conn.close()
    return render_template("admin_dashboard.html", seating_chart=seating_chart, sales=sales)
def get_cost_matrix():
    matrix = [[100, 75, 50, 100] for row in range(12)]
    return matrix
def generate_eticket_number(passenger_name):
    name_parts = passenger_name.replace(" ", "")  # Remove spaces for continuous formatting
    random_case_name = ''.join(
        random.choice([char.upper(), char.lower()]) for char in name_parts
    )
    random_number = random.randint(1000, 9999)
    ticket_number = f"{random_case_name}{random_number}"
    return ticket_number
@app.route("/reserve", methods=["GET", "POST"])
def reserve():
    conn = get_db_connection()
    cursor = conn.cursor()

    matrix = get_cost_matrix()
    seating_chart = [['0' for _ in range(4)] for _ in range(12)]
    cursor.execute("SELECT seatRow, seatColumn FROM reservations")
    reserved = cursor.fetchall()
    for seat in reserved:
        row, col = seat
        seating_chart[row-1][col-1] = 'X'
    seat_row = None
    seat_column = None
    message = None
    if request.method=="POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        passenger_name = f"{first_name} {last_name}"
        seat_row = int(request.form["seat_row"]) - 1
        seat_column = int(request.form["seat_column"])- 1
        
        if 0<= seat_row < 12 and 0<=seat_column <4:
            if seating_chart[seat_row][seat_column] =='X':
                message = "Seat already reserved"
            else:
                price = matrix[seat_row][seat_column]
                eTicketNumber = generate_eticket_number(passenger_name)
                try:
                    cursor.execute(
                         "INSERT INTO reservations (passengerName, seatRow, seatColumn, price, eTicketNumber) VALUES (?, ?, ?, ?,?)",
                        (passenger_name, seat_row + 1, seat_column + 1, price, eTicketNumber)
                    )
                    conn.commit()
                    message = f"Congratualtion {passenger_name}! Row: {seat_row + 1} Seat:{seat_column +1} is now reserved for you.<br> Your ticket number is: {eTicketNumber}"
                except sqlite3.IntegrityError:
                    message= "Seat already taken"
                    
        else:
            message = "Invalid seat selection"
        conn.close()
    return render_template("reserve.html", seating_chart=seating_chart, message=message)


app.run(host="0.0.0.0")
