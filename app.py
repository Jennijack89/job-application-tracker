# JobAppTrack
#CPSC 4205 - IT CapStone Project
#Spring Semester 2026
# Jennifer, Honey, Tyree,Zion

# Import Flask items, SQlite, and Hashing
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

#Assign Flask to app
app = Flask(__name__)
app.secret_key = "dev-secret-change-this" #needed for flash + session

#Assign database file to DB_NAME
DB_NAME = "app.db"

# Connects to my DB in SQlite and Returns....
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user(
        user_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
        )""")

    # future tables fo here too.....
    # conn.execute("""CREATE TABLE IF NOT EXISTS...""")
    
    conn.commit()
    conn.close()
    
    init_db()
   

## My Routes
@app.route("/")
def home():
    return render_template("register.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
