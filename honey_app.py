import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_NAME = "database/app.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create table if it doesn't exist (NEW schema includes apply_date)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            job_title TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL,
            apply_date TEXT NOT NULL
        )
    """)
    conn.commit()

    # --- MIGRATION: add apply_date if old DB doesn't have it ---
    cur.execute("PRAGMA table_info(applications)")
    columns = [row["name"] for row in cur.fetchall()]

    if "apply_date" not in columns:
        cur.execute("ALTER TABLE applications ADD COLUMN apply_date TEXT")
        conn.commit()

        # If old rows exist, fill empty apply_date with today's date-like placeholder
        # (you can change this later if you want)
        cur.execute("UPDATE applications SET apply_date = COALESCE(apply_date, date('now'))")
        conn.commit()

    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()
    applications = conn.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()

    total = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    applied = conn.execute("SELECT COUNT(*) FROM applications WHERE status='Applied'").fetchone()[0]
    interview = conn.execute("SELECT COUNT(*) FROM applications WHERE status='Interview'").fetchone()[0]
    offer = conn.execute("SELECT COUNT(*) FROM applications WHERE status='Offer'").fetchone()[0]
    rejected = conn.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'").fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        applications=applications,
        total=total,
        applied=applied,
        interview=interview,
        offer=offer,
        rejected=rejected
    )


@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        company = request.form["company"].strip()
        job_title = request.form["job_title"].strip()
        location = request.form["location"].strip()
        status = request.form["status"].strip()
        apply_date = request.form["apply_date"].strip()

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO applications (company, job_title, location, status, apply_date) VALUES (?, ?, ?, ?, ?)",
            (company, job_title, location, status, apply_date)
        )
        conn.commit()
        conn.close()

        # ✅ After saving, go back to dashboard (Issue #78 behavior)
        return redirect(url_for("index"))

    return render_template("add_application.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    conn = get_db_connection()
    application = conn.execute("SELECT * FROM applications WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        company = request.form["company"].strip()
        job_title = request.form["job_title"].strip()
        location = request.form["location"].strip()
        status = request.form["status"].strip()
        apply_date = request.form["apply_date"].strip()

        conn.execute("""
            UPDATE applications
            SET company=?, job_title=?, location=?, status=?, apply_date=?
            WHERE id=?
        """, (company, job_title, location, status, apply_date, id))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()
    return render_template("edit_application.html", application=application)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_application(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM applications WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)