from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "jobs.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            job_title TEXT NOT NULL,
            location TEXT,
            status TEXT,
            apply_date TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    conn = get_db_connection()

    applications = conn.execute(
        "SELECT * FROM applications ORDER BY id DESC"
    ).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) FROM applications"
    ).fetchone()[0]

    interview = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status='Interview'"
    ).fetchone()[0]

    offer = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status='Offer'"
    ).fetchone()[0]

    rejected = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status='Rejected'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        applications=applications,
        total=total,
        interview=interview,
        offer=offer,
        rejected=rejected
    )


@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        company = request.form["company"]
        job_title = request.form["job_title"]
        location = request.form["location"]
        status = request.form["status"]
        apply_date = request.form["apply_date"]

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO applications (company, job_title, location, status, apply_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (company, job_title, location, status, apply_date)
        )
        conn.commit()
        conn.close()

        # TASK 6: redirect user to dashboard once successful
        return redirect(url_for("index"))

    return render_template("add_application.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    conn = get_db_connection()
    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        company = request.form["company"]
        job_title = request.form["job_title"]
        location = request.form["location"]
        status = request.form["status"]
        apply_date = request.form["apply_date"]

        conn.execute(
            """
            UPDATE applications
            SET company = ?, job_title = ?, location = ?, status = ?, apply_date = ?
            WHERE id = ?
            """,
            (company, job_title, location, status, apply_date, id)
        )
        conn.commit()
        conn.close()

        # TASK 6 also works here after update
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit_application.html", application=application)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_application(id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM applications WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)