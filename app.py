# JobAppTrack
#CPSC 4205 - IT CapStone Project
#Spring Semester 2026
# Jennifer, Honey, Tyree,Zion

# Import Flask items, SQlite, and Hashing

import os
import smtplib
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "patelhoney1209@gmail.com"
SMTP_PASSWORD = "gbhqxuctnvftxxps"
EMAIL_FROM = "patelhoney1209@gmail.com"
SMTP_USE_TLS = True
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-this")

DB_NAME = "database/app.db"



def send_reset_code(to_email, code):
    subject = "Password Reset Code"
    body = f"Your password reset code is: {code}\n\nThis code expires in 15 minutes."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email failed:", e)
        
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def column_exists(conn, table_name, column_name):
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(col[1] == column_name for col in columns)


def ensure_column(conn, table_name, column_name, definition):
    if not column_exists(conn, table_name, column_name):
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def init_db():
    conn = get_db_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            user_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            reset_code_hash TEXT,
            reset_code_expiry TEXT
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS applications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            job_title TEXT,
            location TEXT,
            status TEXT,
            apply_date TEXT,
            user_id INTEGER
        )
        """
    )

    # Backfill older project databases safely.
    ensure_column(conn, "users", "reset_code_hash", "TEXT")
    ensure_column(conn, "users", "reset_code_expiry", "TEXT")

    ensure_column(conn, "applications", "job_title", "TEXT")
    ensure_column(conn, "applications", "location", "TEXT")
    ensure_column(conn, "applications", "status", "TEXT")
    ensure_column(conn, "applications", "apply_date", "TEXT")
    ensure_column(conn, "applications", "user_id", "INTEGER")

    conn.commit()
    conn.close()


init_db()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


def send_reset_code_email(recipient_email, code):
    """Returns (email_sent, error_message)."""
    if not all([SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM]):
        print("\n=== Password Reset Code (SMTP not configured) ===")
        print(f"Email: {recipient_email}")
        print(f"Code: {code}")
        print("===============================================\n")
        return False, "SMTP is not configured yet."

    msg = EmailMessage()
    msg["Subject"] = "Your JobAppTrack password reset code"
    msg["From"] = EMAIL_FROM
    msg["To"] = recipient_email
    msg.set_content(
        f"Your JobAppTrack password reset code is: {code}\n\n"
        "This code expires in 15 minutes.\n"
        "If you did not request a password reset, you can ignore this email."
    )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True, ""
    except Exception as exc:
        print("Failed to send reset code email:", exc)
        print("\n=== Password Reset Code (email send failed) ===")
        print(f"Email: {recipient_email}")
        print(f"Code: {code}")
        print("=============================================\n")
        return False, str(exc)


def get_current_user_application(conn, app_id, user_id):
    return conn.execute(
        "SELECT * FROM applications WHERE id = ? AND user_id = ?",
        (app_id, user_id),
    ).fetchone()


@app.route("/")
def home():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username_or_email = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username_or_email,),
        ).fetchone()

        if not user:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (username_or_email.lower(),),
            ).fetchone()

        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_ID"]
            session["username"] = user["username"]
            flash("Login successful.")
            return redirect(url_for("dashboard"))

        flash("Invalid username/email or password.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not email or not password or not confirm:
            flash("All fields are required.")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return render_template("register.html")

        conn = get_db_connection()
        existing = conn.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, email),
        ).fetchone()

        if existing:
            conn.close()
            flash("Username or email already exists.")
            return render_template("register.html")

        password_hash = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        conn.commit()
        conn.close()

        flash("Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    dev_reset_code = None

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if not email:
            flash("Please enter your email address.")
            return render_template("forgot_password.html")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user:
            code = f"{random.randint(0, 999999):06d}"
            expires_at = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
            conn.execute(
                """
                UPDATE users
                SET reset_code_hash = ?, reset_code_expiry = ?
                WHERE user_ID = ?
                """,
                (generate_password_hash(code), expires_at, user["user_ID"]),
            )
            conn.commit()
            email_sent, send_error = send_reset_code_email(email, code)
            if not email_sent:
                dev_reset_code = code
                flash(
                    "Code generated. Email is not configured yet, so the code is shown below for local testing."
                )
            else:
                flash("A 6-digit reset code has been sent to your email.")
        else:
            flash("If that email exists, a 6-digit reset code has been sent.")

        conn.close()
        return render_template(
            "forgot_password.html",
            email=email,
            dev_reset_code=dev_reset_code,
        )

    return render_template("forgot_password.html")


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email", request.form.get("email", "")).strip().lower()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        code = request.form.get("code", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not email or not code or not password or not confirm:
            flash("All fields are required.")
            return render_template("reset_password.html", email=email)

        if password != confirm:
            flash("Passwords do not match.")
            return render_template("reset_password.html", email=email)

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return render_template("reset_password.html", email=email)

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if not user or not user["reset_code_hash"] or not user["reset_code_expiry"]:
            conn.close()
            flash("Invalid or expired reset code.")
            return render_template("reset_password.html", email=email)

        try:
            expires_at = datetime.fromisoformat(user["reset_code_expiry"])
        except ValueError:
            expires_at = datetime.utcnow() - timedelta(seconds=1)

        if expires_at < datetime.utcnow():
            conn.execute(
                "UPDATE users SET reset_code_hash = NULL, reset_code_expiry = NULL WHERE user_ID = ?",
                (user["user_ID"],),
            )
            conn.commit()
            conn.close()
            flash("That reset code has expired. Please request a new one.")
            return redirect(url_for("forgot_password"))

        if not check_password_hash(user["reset_code_hash"], code):
            conn.close()
            flash("Invalid or expired reset code.")
            return render_template("reset_password.html", email=email)

        conn.execute(
            """
            UPDATE users
            SET password_hash = ?, reset_code_hash = NULL, reset_code_expiry = NULL
            WHERE user_ID = ?
            """,
            (generate_password_hash(password), user["user_ID"]),
        )
        conn.commit()
        conn.close()

        flash("Password reset successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("reset_password.html", email=email)


@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    conn = get_db_connection()

    applications = conn.execute(
        "SELECT * FROM applications WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    ).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE user_id = ?",
        (user_id,),
    ).fetchone()[0]
    interview = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status='Interview'",
        (user_id,),
    ).fetchone()[0]
    offer = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status='Offer'",
        (user_id,),
    ).fetchone()[0]
    rejected = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status='Rejected'",
        (user_id,),
    ).fetchone()[0]
    waiting = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE user_id = ? AND status='Applied'",
        (user_id,),
    ).fetchone()[0]

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week_str = start_of_week.isoformat()

    applied_this_week = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE user_id = ? AND apply_date >= ?",
        (user_id, start_of_week_str),
    ).fetchone()[0]

    reminder_messages = []
    if interview > 0:
        reminder_messages.append("Remember to follow up within 2-3 days after your interview.")
    if offer > 0:
        reminder_messages.append("Review your offer details and keep track of any deadlines.")
    if waiting > 0:
        reminder_messages.append("Check in on applications that have been waiting for a response.")
    if rejected > 0:
        reminder_messages.append("Keep going and continue applying to new opportunities.")
    if total == 0:
        reminder_messages.append("Start adding applications to begin tracking your progress.")

    weekly_data_rows = conn.execute(
        """
        SELECT
            strftime('%m', apply_date) AS month_num,
            CAST(((CAST(strftime('%d', apply_date) AS INTEGER) - 1) / 7) + 1 AS INTEGER) AS week_of_month,
            COUNT(*) AS count
        FROM applications
        WHERE user_id = ? AND apply_date IS NOT NULL AND apply_date != ''
        GROUP BY month_num, week_of_month
        ORDER BY month_num, week_of_month
        """,
        (user_id,),
    ).fetchall()

    month_names = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }

    weekly_data = [
        {
            "label": f"{month_names.get(row['month_num'], row['month_num'])} Week {row['week_of_month']}",
            "count": row["count"],
        }
        for row in weekly_data_rows
    ]

    conn.close()

    return render_template(
        "dashboard.html",
        applications=applications,
        total=total,
        interview=interview,
        offer=offer,
        rejected=rejected,
        waiting=waiting,
        applied_this_week=applied_this_week,
        weekly_data=weekly_data,
        reminder_messages=reminder_messages,
    )


@app.route("/applications")
@login_required
def view_app():
    conn = get_db_connection()
    applications = conn.execute(
        "SELECT * FROM applications WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],),
    ).fetchall()
    conn.close()
    return render_template("view_app.html", applications=applications)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_application():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        job_title = request.form.get("job_title", "").strip()
        location = request.form.get("location", "").strip()
        status = request.form.get("status", "").strip()
        apply_date = request.form.get("apply_date", "").strip()

        if not company or not job_title or not location or not status or not apply_date:
            flash("All application fields are required.")
            return render_template("add_application.html")

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO applications (company, job_title, location, status, apply_date, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (company, job_title, location, status, apply_date, session["user_id"]),
        )
        conn.commit()
        conn.close()

        flash("Application added successfully.")
        return redirect(url_for("view_app"))

    return render_template("add_application.html")


@app.route("/edit/<int:app_id>", methods=["GET", "POST"])
@login_required
def edit_application(app_id):
    conn = get_db_connection()
    application = get_current_user_application(conn, app_id, session["user_id"])

    if not application:
        conn.close()
        flash("Application not found.")
        return redirect(url_for("view_app"))

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        job_title = request.form.get("job_title", "").strip()
        location = request.form.get("location", "").strip()
        status = request.form.get("status", "").strip()
        apply_date = request.form.get("apply_date", "").strip()

        if not company or not job_title or not location or not status or not apply_date:
            conn.close()
            flash("All application fields are required.")
            return render_template("edit_application.html", application=application)

        conn.execute(
            """
            UPDATE applications
            SET company = ?, job_title = ?, location = ?, status = ?, apply_date = ?
            WHERE id = ? AND user_id = ?
            """,
            (company, job_title, location, status, apply_date, app_id, session["user_id"]),
        )
        conn.commit()
        conn.close()
        flash("Application updated successfully.")
        return redirect(url_for("view_app"))

    conn.close()
    return render_template("edit_application.html", application=application)


@app.route("/delete/<int:app_id>", methods=["POST"])
@login_required
def delete_application(app_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM applications WHERE id = ? AND user_id = ?",
        (app_id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    flash("Application deleted.")
    return redirect(url_for("view_app"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
