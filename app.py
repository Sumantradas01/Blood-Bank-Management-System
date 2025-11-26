from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"  # change in production

# ------------------------------------
# DATABASE CONNECTION
# ------------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",          # set your MySQL password if any
    database="bloodbank1"
)
cursor = db.cursor(dictionary=True)

# ------------------------------------
# HOME PAGE
# ------------------------------------
@app.route("/")
def home():
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

        if not name or not email or not phone or not password or not blood_group:
            flash("All fields are required for donor registration.")
            return redirect(url_for("donor_register"))

        try:
            cursor.execute(
                "INSERT INTO donors (name, email, phone, password, blood_group) VALUES (%s, %s, %s, %s, %s)",
                (name, email, phone, password, blood_group)
            )
            db.commit()
            flash("Donor registered successfully!")
            return redirect(url_for("donor_login"))

        except Exception as e:
            db.rollback()
            app.logger.error("DB error (donor_register): %s", e)
            flash("Database error: " + str(e))
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
            flash("Provide both email and password.")
            return redirect(url_for("donor_login"))

        try:
            cursor.execute("SELECT * FROM donors WHERE email=%s AND password=%s",
                           (email, password))
            user = cursor.fetchone()

            if user:
                session["donor_id"] = user.get("donor_id")
                session["donor_name"] = user.get("name")
                flash("Login successful.")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid email or password!")
                return redirect(url_for("donor_login"))

        except Exception as e:
            app.logger.error("DB error (donor_login): %s", e)
            flash("Database error: " + str(e))
            return redirect(url_for("donor_login"))

    return render_template("donor_login.html")


# ------------------------------------
# ADMIN REGISTRATION
# ------------------------------------
@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        admin_name = request.form.get("admin_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        hospital_name = request.form.get("hospital_name")

        if not admin_name or not email or not phone or not password or not hospital_name:
            flash("All fields are required!")
            return redirect(url_for("admin_register"))

        try:
            # Correct parameterized SQL matching your admin table columns
            cursor.execute("""
                INSERT INTO admin (hospital_name, admin_name, email, phone, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (hospital_name, admin_name, email, phone, password))
            db.commit()
            flash("Admin Registered Successfully!")
            return redirect(url_for("admin_login"))

        except Exception as e:
            db.rollback()
            app.logger.error("DB error (admin_register): %s", e)
            flash("Database error: " + str(e))
            return redirect(url_for("admin_register"))

    return render_template("admin_register.html")


# ------------------------------------
# ADMIN LOGIN
# ------------------------------------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        # Accept admin_name (preferred) or username if your HTML uses that
        admin_name = request.form.get("admin_name") or request.form.get("username")
        password = request.form.get("password")

        if not admin_name or not password:
            flash("Provide admin name and password.")
            return redirect(url_for("admin_login"))

        try:
            cursor.execute("""
                SELECT * FROM admin
                WHERE admin_name=%s AND password=%s
            """, (admin_name, password))

            data = cursor.fetchone()
            if data:
                session["admin_id"] = data.get("admin_id")
                session["admin_name"] = data.get("admin_name")
                flash("Login Successful!")
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Invalid Admin Name or Password!")
                return redirect(url_for("admin_login"))

        except Exception as e:
            app.logger.error("DB error (admin_login): %s", e)
            flash("Database error: " + str(e))
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


# ------------------------------------
# SEARCH BLOOD
# ------------------------------------
@app.route("/search_blood")
def search_blood():
    return render_template("search_blood.html")


# ------------------------------------
# HOSPITAL LOGIN
# ------------------------------------
@app.route("/hospital_login")
def hospital_login():
    return render_template("hospital_login.html")


# ------------------------------------
# Simple public dashboard
# ------------------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ----------------------------------------
# ADMIN DASHBOARD (main unified route)
# ----------------------------------------
@app.route("/admin_dashboard")
def admin_dashboard():
    try:
        cursor.execute("SELECT * FROM blood_stock")
        blood_stock = cursor.fetchall()

        cursor.execute("""
            SELECT bo.*, h.hospital_name 
            FROM blood_orders bo
            LEFT JOIN hospitals h ON bo.hospital_id = h.hospital_id
            ORDER BY bo.request_date DESC
        """)
        orders = cursor.fetchall()

        cursor.execute("""
            SELECT br.*, h.hospital_name 
            FROM blood_requests br
            LEFT JOIN hospitals h ON br.hospital_id = h.hospital_id
            ORDER BY br.request_date DESC
        """)
        requirements = cursor.fetchall()

        cursor.execute("SELECT * FROM donors ORDER BY donor_id DESC")
        donors = cursor.fetchall()

        return render_template(
            "admin_dashboard.html",
            blood_stock=blood_stock,
            orders=orders,
            requirements=requirements,
            donors=donors
        )

    except Exception as e:
        app.logger.error("DB error (admin_dashboard): %s", e)
        flash("Database error: " + str(e))
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
        cursor.execute("UPDATE blood_orders SET status=%s WHERE order_id=%s", (status, order_id))
        db.commit()
        flash(f"Order {order_id} updated to {status}.")
    except Exception as e:
        db.rollback()
        app.logger.error("DB error (update_order): %s", e)
        flash("Database error: " + str(e))

    return redirect(url_for("admin_dashboard"))


@app.route("/delete_donor/<int:donor_id>")
def delete_donor(donor_id):
    try:
        cursor.execute("DELETE FROM donors WHERE donor_id=%s", (donor_id,))
        db.commit()
        flash("Donor removed.")
    except Exception as e:
        db.rollback()
        app.logger.error("DB error (delete_donor): %s", e)
        flash("Database error: " + str(e))

    return redirect(url_for("admin_dashboard"))


@app.route("/update_stock/<int:stock_id>", methods=["POST"])
def update_stock(stock_id):
    units_raw = request.form.get("units")
    if units_raw is None:
        flash("Units value missing.")
        return redirect(url_for("admin_dashboard"))

    try:
        units = int(units_raw)
        if units < 0:
            raise ValueError("Units cannot be negative.")

        cursor.execute("UPDATE blood_stock SET units=%s WHERE stock_id=%s", (units, stock_id))
        db.commit()
        flash("Stock updated successfully.")
    except ValueError:
        flash("Units must be a non-negative integer.")
    except Exception as e:
        db.rollback()
        app.logger.error("DB error (update_stock): %s", e)
        flash("Database error: " + str(e))

    return redirect(url_for("admin_dashboard"))


# ------------------------------------
# LOGOUT (admin & donor)
# ------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("home"))


# ------------------------------------
# RUN APP
# ------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
