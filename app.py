from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ------------------------------------
# DATABASE CONNECTION
# ------------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
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
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        blood_group = request.form["blood_group"]

        cursor.execute(
            "INSERT INTO donors (name, email, phone, password, blood_group) VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone, password, blood_group)
        )
        db.commit()

        flash("Donor registered successfully!")
        return redirect(url_for("donor_login"))

    return render_template("donor_register.html")

# ------------------------------------
# DONOR LOGIN
# ------------------------------------
@app.route("/donor_login", methods=["GET", "POST"])
def donor_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cursor.execute("SELECT * FROM donors WHERE email=%s AND password=%s",
                       (email, password))
        user = cursor.fetchone()

        if user:
            return render_template("donor_dashboard.html")
        else:
            flash("Invalid email or password!")
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

        cursor.execute("""
            INSERT INTO admin (hospital_name, admin_name, email, phone, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (hospital_name, admin_name, email, phone, password))

        db.commit()
        flash("Admin Registered Successfully!")
        return redirect(url_for("admin_login"))

    return render_template("admin_register.html")

# ------------------------------------
# ADMIN LOGIN
# ------------------------------------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":

        admin_name = request.form.get("username")
        password = request.form.get("password")

        cursor.execute("""
            SELECT * FROM admin
            WHERE admin_name=%s AND password=%s
        """, (admin_name, password))

        data = cursor.fetchone()

        if data:
            flash("Login Successful!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Admin Name or Password!")
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

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/hospital_register', methods=['GET', 'POST'])
def hospital_register():
    if request.method == 'POST':
        name = request.form['name']
        reg_no = request.form['reg_no']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO hospital (name, reg_no, email, phone, password) VALUES (%s, %s, %s, %s, %s)",
                    (name, reg_no, email, phone, password))
        mysql.connection.commit()
        cur.close()

        flash("Hospital registered successfully!")
        return redirect(url_for('hospital_login'))

    return render_template('hospital_register.html')


# ------------------------------------
# RUN APP
# ------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
