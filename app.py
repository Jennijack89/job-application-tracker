# JobAppTrack
#CPSC 4205 - IT CapStone Project
#Spring Semester 2026
# Jennifer, Honey, Tyree,Zion

# Import Flask items, SQlite, and Hashing
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

#Assign Flask to app
app = Flask(__name__)
app.secret_key = "dev-secret-change-this" #needed for flash + session

#Assign database file to DB_NAME
DB_NAME = "app.db"
### These were to check which database the info was saved to, confirmed it was a different one and moved that one to folder
#print("CWD:", os.getcwd())
#print("DB path", os.path.abspath(DB_NAME))

# Connects to my DB in SQlite and Returns....
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
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
    return redirect(url_for("register"))


## Get the input create account data saves it in variables to be used in table
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password","")
        confirm = request.form.get("confirm_password","")

        #1) validation
        if not username or not email or not password or not confirm:
            flash("All fields are required.")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.")
            return render_template("register.html")

        if len(password)< 8:
            flash("Password must be at least 8 characters.")
            return render_template("register.html")

        #2) Check if the username/email exists
        conn = get_db_connection()
        existing = conn.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",(username,email)
            ).fetchone()

        if existing:
            conn.close()
            flash("Username or email already exists.")
            return render_template("register.html")

        #3) Hash password and store user
        password_hash = generate_password_hash(password)

        #) Insert Input into users Table in SQlite
        conn.execute(
            "INSERT INTO users (username,email,password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
            )
            
        conn.commit()
        conn.close()

        flash("Account created! Please log in.")
        return redirect(url_for("register")) #change to redirect to Login when created
    
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
