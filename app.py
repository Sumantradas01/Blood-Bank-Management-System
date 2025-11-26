# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change_this_in_production"

# ------------------------------------
# DATABASE CONNECTION (single connection)
# ------------------------------------
def get_db_connection():
    # you can wrap this to reconnect if needed
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # set your MySQL password if any
        database="bloodbank1",
        autocommit=False
    )

# create initial connection and cursor
try:
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
except Error as e:
    # If DB isn't available, log and keep variables None for graceful errors
    app.logger.error("Initial DB connection error: %s", e)
    db = None
    cursor = None


# helper to ensure we have a working cursor (reconnect if closed)
def get_cursor():
    global db, cursor
    try:
        if db is None or not db.is_connected():
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
    except Exception as e:
        app.logger.error("DB reconnect error: %s", e)
        raise
    return db, cursor


# ------------------------------------
# HOME PAGE
# ------------------------------------
@app.route("/")
def home():
    # main homepage (index)
    return render_template("index.html")


# ------------------------------------
# DONOR REGISTRATION
# ------------------------------------
@app.route("/donor_register", methods=["GET", "POST"])
def donor_register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        blood_group = request.form.get("blood_group")

        if not (name and email and phone and password and blood_group):
            flash("All fields are required for donor registration.", "error")
            return redirect(url_for("donor_register"))

        try:
            db, cur = get_cursor()
            hashed = generate_password_hash(password)
            cur.execute(
                "INSERT INTO donors (name, email, phone, password, blood_group) VALUES (%s, %s, %s, %s, %s)",
                (name, email, phone, hashed, blood_group)
            )
            db.commit()
            flash("Donor registered successfully!", "success")
            return redirect(url_for("donor_login"))

        except Exception as e:
            if db:
                db.rollback()
            app.logger.error("DB error (donor_register): %s", e)
            flash("Database error: " + str(e), "error")
            return redirect(url_for("donor_register"))

    return render_template("donor_register.html")


# ------------------------------------
# DONOR LOGIN
# ------------------------------------
@app.route("/donor_login", methods=["GET", "POST"])
def donor_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Provide both email and password.", "error")
            return redirect(url_for("donor_login"))

        try:
            db, cur = get_cursor()
            cur.execute("SELECT * FROM donors WHERE email=%s", (email,))
            user = cur.fetchone()

            if user and check_password_hash(user.get("password"), password):
                session.clear()
                session["donor_id"] = user.get("donor_id")
                session["donor_name"] = user.get("name")
                flash("Login successful.", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid email or password!", "error")
                return redirect(url_for("donor_login"))

        except Exception as e:
            app.logger.error("DB error (donor_login): %s", e)
            flash("Database error: " + str(e), "error")
            return redirect(url_for("donor_login"))

    return render_template("donor_login.html")


# ------------------------------------
# ADMIN REGISTRATION
# ------------------------------------
@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        hospital_name = request.form.get("hospital_name")
        admin_name = request.form.get("admin_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        if not (hospital_name and admin_name and email and phone and password):
            flash("All fields are required!", "error")
            return redirect(url_for("admin_register"))

        try:
            db, cur = get_cursor()
            hashed = generate_password_hash(password)
            cur.execute("""
                INSERT INTO admin (hospital_name, admin_name, email, phone, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (hospital_name, admin_name, email, phone, hashed))
            db.commit()
            flash("Admin Registered Successfully!", "success")
            return redirect(url_for("admin_login"))

        except Exception as e:
            if db:
                db.rollback()
            app.logger.error("DB error (admin_register): %s", e)
            flash("Database error: " + str(e), "error")
            return redirect(url_for("admin_register"))

    return render_template("admin_register.html")


# ------------------------------------
# ADMIN LOGIN
# ------------------------------------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_name = request.form.get("admin_name") or request.form.get("username")
        password = request.form.get("password")

        if not admin_name or not password:
            flash("Provide admin name and password.", "error")
            return redirect(url_for("admin_login"))

        try:
            db, cur = get_cursor()
            cur.execute("SELECT * FROM admin WHERE admin_name=%s", (admin_name,))
            data = cur.fetchone()
            if data and check_password_hash(data.get("password"), password):
                session.clear()
                session["admin_id"] = data.get("admin_id")
                session["admin_name"] = data.get("admin_name")
                flash("Login Successful!", "success")
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Invalid Admin Name or Password!", "error")
                return redirect(url_for("admin_login"))

        except Exception as e:
            app.logger.error("DB error (admin_login): %s", e)
            flash("Database error: " + str(e), "error")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


# ------------------------------------
# SEARCH BLOOD
# ------------------------------------
@app.route("/search_blood")
def search_blood():
    return render_template("search_blood.html")


# ------------------------------------
# PUBLIC DASHBOARD
# ------------------------------------
@app.route("/dashboard")
def dashboard():
    # simple public donor/dashboard page
    return render_template("dashboard.html")


# -------------------------------------------------
# HOSPITAL REGISTRATION & LOGIN & DASHBOARD
# -------------------------------------------------
@app.route("/hospital_register", methods=["GET", "POST"])
def hospital_register():
    if request.method == "POST":
        hospital_name = request.form.get("hospital_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        username = request.form.get("username")
        password = request.form.get("password")

        if not (hospital_name and email and phone and address and username and password):
            flash("All fields are required!", "error")
            return redirect(url_for("hospital_register"))

        try:
            db, cur = get_cursor()
            hashed = generate_password_hash(password)
            cur.execute("""
                INSERT INTO hospitals (hospital_name, email, phone, address, username, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (hospital_name, email, phone, address, username, hashed))
            db.commit()
            flash("Hospital Registered Successfully!", "success")
            return redirect(url_for("hospital_login"))

        except Exception as e:
            if db:
                db.rollback()
            app.logger.error("DB error (hospital_register): %s", e)
            flash("Database Error: " + str(e), "error")
            return redirect(url_for("hospital_register"))

    return render_template("hospital_register.html")


@app.route("/hospital_login", methods=["GET", "POST"])
def hospital_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Enter Username and Password", "error")
            return redirect(url_for("hospital_login"))

        try:
            db, cur = get_cursor()
            cur.execute("SELECT * FROM hospitals WHERE username=%s", (username,))
            hospital = cur.fetchone()

            if hospital and check_password_hash(hospital.get("password"), password):
                session.clear()
                session["hospital_id"] = hospital["hospital_id"]
                session["hospital_name"] = hospital["hospital_name"]
                flash("Login Successful!", "success")
                return redirect(url_for("hospital_dashboard"))
            else:
                flash("Invalid Username or Password!", "error")
                return redirect(url_for("hospital_login"))

        except Exception as e:
            app.logger.error("DB error (hospital_login): %s", e)
            flash("Database Error: " + str(e), "error")
            return redirect(url_for("hospital_login"))

    return render_template("hospital_login.html")


@app.route("/hospital_dashboard")
def hospital_dashboard():
    if "hospital_id" not in session:
        flash("Please login first!", "error")
        return redirect(url_for("hospital_login"))

    hospital_id = session["hospital_id"]

    try:
        db, cur = get_cursor()
        cur.execute("""
            SELECT * FROM blood_orders
            WHERE hospital_id = %s
            ORDER BY request_date DESC
        """, (hospital_id,))
        orders = cur.fetchall()

        return render_template(
            "hospital_dashboard.html",
            hospital_name=session.get("hospital_name"),
            orders=orders
        )

    except Exception as e:
        app.logger.error("DB error (hospital_dashboard): %s", e)
        flash("Database Error: " + str(e), "error")
        return render_template(
            "hospital_dashboard.html",
            hospital_name=session.get("hospital_name"),
            orders=[]
        )


# ----------------------------------------
# ADMIN DASHBOARD
# ----------------------------------------
@app.route("/admin_dashboard")
def admin_dashboard():
    try:
        db, cur = get_cursor()

        cur.execute("SELECT * FROM blood_stock")
        blood_stock = cur.fetchall()

        cur.execute("""
            SELECT bo.*, h.hospital_name 
            FROM blood_orders bo
            LEFT JOIN hospitals h ON bo.hospital_id = h.hospital_id
            ORDER BY bo.request_date DESC
        """)
        orders = cur.fetchall()

        cur.execute("""
            SELECT br.*, h.hospital_name 
            FROM blood_requests br
            LEFT JOIN hospitals h ON br.hospital_id = h.hospital_id
            ORDER BY br.request_date DESC
        """)
        requirements = cur.fetchall()

        cur.execute("SELECT * FROM donors ORDER BY donor_id DESC")
        donors = cur.fetchall()

        return render_template(
            "admin_dashboard.html",
            blood_stock=blood_stock,
            orders=orders,
            requirements=requirements,
            donors=donors
        )

    except Exception as e:
        app.logger.error("DB error (admin_dashboard): %s", e)
        flash("Database error: " + str(e), "error")
        return render_template(
            "admin_dashboard.html",
            blood_stock=[], orders=[], requirements=[], donors=[]
        )


# ------------------------------------
# ORDERS / STOCK / DONOR MANAGEMENT
# ------------------------------------
@app.route("/update_order/<int:order_id>/<action>")
def update_order(order_id, action):
    if action == "approve":
        status = "Approved"
    elif action == "reject":
        status = "Rejected"
    elif action == "complete":
        status = "Completed"
    else:
        status = "Pending"

    try:
        db, cur = get_cursor()
        cur.execute("UPDATE blood_orders SET status=%s WHERE order_id=%s", (status, order_id))
        db.commit()
        flash(f"Order {order_id} updated to {status}.", "success")
    except Exception as e:
        if db:
            db.rollback()
        app.logger.error("DB error (update_order): %s", e)
        flash("Database error: " + str(e), "error")

    return redirect(url_for("admin_dashboard"))


@app.route("/delete_donor/<int:donor_id>")
def delete_donor(donor_id):
    try:
        db, cur = get_cursor()
        cur.execute("DELETE FROM donors WHERE donor_id=%s", (donor_id,))
        db.commit()
        flash("Donor removed.", "success")
    except Exception as e:
        if db:
            db.rollback()
        app.logger.error("DB error (delete_donor): %s", e)
        flash("Database error: " + str(e), "error")

    return redirect(url_for("admin_dashboard"))


@app.route("/update_stock/<int:stock_id>", methods=["POST"])
def update_stock(stock_id):
    units_raw = request.form.get("units")
    if units_raw is None:
        flash("Units value missing.", "error")
        return redirect(url_for("admin_dashboard"))

    try:
        units = int(units_raw)
        if units < 0:
            raise ValueError("Units cannot be negative.")

        db, cur = get_cursor()
        cur.execute("UPDATE blood_stock SET units=%s WHERE stock_id=%s", (units, stock_id))
        db.commit()
        flash("Stock updated successfully.", "success")
    except ValueError:
        flash("Units must be a non-negative integer.", "error")
    except Exception as e:
        if db:
            db.rollback()
        app.logger.error("DB error (update_stock): %s", e)
        flash("Database error: " + str(e), "error")

    return redirect(url_for("admin_dashboard"))


# ------------------------------------
# LOGOUT
# ------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))


# ------------------------------------
# RUN APP
# ------------------------------------
if __name__ == "__main__":
    # debug True for development only; change in production
    app.run(debug=True)
