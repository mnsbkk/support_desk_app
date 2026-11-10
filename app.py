import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

# App settings and valid ticket states.
DATABASE = "tickets.db"
STATUS_OPTIONS = ["Open", "In Progress", "Resolved", "Closed"]


# Keep a single SQLite connection per request.
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Create the database schema if it doesn't exist yet.
def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ticket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tickets")
def list_tickets():
    db = get_db()
    tickets = db.execute(
        "SELECT * FROM ticket ORDER BY created_at DESC"
    ).fetchall()
    return render_template("list.html", tickets=tickets)


# Create a new support ticket from the submission form.
@app.route("/tickets/new", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        description = request.form.get("description", "").strip()

        if not all([name, email, subject, description]):
            flash("All fields are required.", "error")
            return render_template(
                "create.html",
                form=request.form,
            )

        now = datetime.utcnow().isoformat(timespec="seconds")
        db = get_db()
        cur = db.execute(
            """INSERT INTO ticket (name, email, subject, description, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, 'Open', ?, ?)""",
            (name, email, subject, description, now, now),
        )
        db.commit()
        flash("Ticket submitted successfully!", "success")
        return redirect(url_for("detail_ticket", ticket_id=cur.lastrowid))

    return render_template("create.html", form={})


@app.route("/tickets/<int:ticket_id>")
def detail_ticket(ticket_id):
    db = get_db()
    ticket = db.execute(
        "SELECT * FROM ticket WHERE id = ?", (ticket_id,)
    ).fetchone()
    if ticket is None:
        flash("Ticket not found.", "error")
        return redirect(url_for("list_tickets"))
    return render_template("detail.html", ticket=ticket)


@app.route("/tickets/<int:ticket_id>/edit", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    db = get_db()
    ticket = db.execute(
        "SELECT * FROM ticket WHERE id = ?", (ticket_id,)
    ).fetchone()
    if ticket is None:
        flash("Ticket not found.", "error")
        return redirect(url_for("list_tickets"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Open")

        if not all([name, email, subject, description]) or status not in STATUS_OPTIONS:
            flash("All fields are required and status must be valid.", "error")
            return render_template(
                "edit.html",
                ticket=ticket,
                form=request.form,
                status_options=STATUS_OPTIONS,
            )

        now = datetime.utcnow().isoformat(timespec="seconds")
        db.execute(
            """UPDATE ticket
               SET name=?, email=?, subject=?, description=?, status=?, updated_at=?
               WHERE id=?""",
            (name, email, subject, description, status, now, ticket_id),
        )
        db.commit()
        flash("Ticket updated successfully!", "success")
        return redirect(url_for("detail_ticket", ticket_id=ticket_id))

    return render_template(
        "edit.html",
        ticket=ticket,
        form=ticket,
        status_options=STATUS_OPTIONS,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)