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

@app.route("/")
def home():
    return render_template("register.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
