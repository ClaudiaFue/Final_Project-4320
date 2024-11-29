import sqlite3
from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route("/")
def home():
    return ""

app.run(host="0.0.0.0")
