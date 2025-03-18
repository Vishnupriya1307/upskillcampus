from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from auth import hash_password, verify_password

# 🔹 Load environment variables
load_dotenv()

# 🔍 Debugging Step: Check if key is loaded correctly
key = os.getenv("FERNET_KEY")

if not key or len(key) != 44:
    raise ValueError(f"❌ Invalid Fernet Key: {key} (Expected 44 characters)")
print("Loaded Key:", key)
print("Key Length:", len(key))


cipher = Fernet(key)  # ✅ Correctly initialize Fernet

# 📌 Define Blueprint for routes
routes = Blueprint("routes", __name__, url_prefix="/")

# 🔗 Database connection function
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🔹 Register route
@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("⚠️ Username and password are required.", "danger")
            return redirect(url_for("routes.register"))

        hashed_password = hash_password(password)

        try:
            with get_db_connection() as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()

            flash("✅ Registration successful! You can now log in.", "success")
            return redirect(url_for("routes.login"))

        except sqlite3.IntegrityError:
            flash("⚠️ Username already exists. Try a different one.", "danger")

    return render_template("register.html")

# 🔹 Dashboard route
@routes.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("⚠️ You must be logged in to access the dashboard.", "danger")
        return redirect(url_for("routes.login"))

    return render_template("dashboard.html", username=session["username"])

# 🔹 Add password route
@routes.route("/add_password", methods=["POST"])
def add_password():
    if "user_id" not in session:
        flash("⚠️ Please log in first.", "danger")
        return redirect(url_for("routes.login"))

    website = request.form.get("website")
    username = request.form.get("username")
    password = request.form.get("password")

    if not website or not username or not password:
        flash("⚠️ All fields are required.", "danger")
        return redirect(url_for("routes.dashboard"))

    encrypted_password = cipher.encrypt(password.encode()).decode()

    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO passwords (user_id, website, username, encrypted_password) VALUES (?, ?, ?, ?)", 
            (session["user_id"], website, username, encrypted_password)
        )
        conn.commit()

    flash("✅ Password added successfully!", "success")
    return redirect(url_for("routes.dashboard"))

# 🔹 Login route
@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("⚠️ Username and password are required.", "danger")
            return redirect(url_for("routes.login"))

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

        if user and verify_password(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("✅ Login successful!", "success")
            return redirect(url_for("routes.dashboard"))

        flash("❌ Invalid username or password. Please try again.", "danger")

    return render_template("login.html")

# 🔹 Logout route
@routes.route("/logout")
def logout():
    session.clear()
    flash("✅ You have been logged out.", "info")
    return redirect(url_for("routes.login"))

# 🔹 View passwords route
@routes.route("/view_passwords")
def view_passwords():
    if "user_id" not in session:
        return redirect(url_for("routes.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT website, username, encrypted_password FROM passwords WHERE user_id = ?", (session["user_id"],))

    passwords = []
    for website, username, encrypted_password in cursor.fetchall():
        try:
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            passwords.append((website, username, decrypted_password))
        except Exception as e:
            print(f"❌ Decryption Error for {website}: {e}")  # ✅ Log decryption error
            passwords.append((website, username, "❌ Error decrypting"))

    conn.close()
    return render_template("view_passwords.html", passwords=passwords)

# 🔹 Initialize routes function
def init_routes(app):
    """Attach Blueprint to Flask app"""
    app.register_blueprint(routes)
