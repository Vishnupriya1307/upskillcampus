from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from cryptography.fernet import Fernet
from routes import routes  # Import Blueprint correctly

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for sessions
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.register_blueprint(routes)  # Register Blueprint

# Generate a new encryption key (for testing purposes)
new_key = Fernet.generate_key()
print("Generated Encryption Key:", new_key.decode())  # Debugging
print(f"Current Working Directory: {os.getcwd()}")  # Debugging


# Database setup (make sure users.db exists)
def init_db():
    DB_PATH = os.path.abspath("C:/Users/vishn/password-manager/users.db")

    # Check if database file exists
    if not os.path.exists(DB_PATH):
        print(f"⚠ Database file not found at {DB_PATH}. Creating a new one...")
        open(DB_PATH, 'w').close()  # Create an empty database file

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create passwords table
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


# Route to the home page (index)
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('routes.dashboard'))  # Redirect to the Blueprint's dashboard
    return render_template('index.html')


# Route to log out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# Run the app
if __name__ == '__main__':
    init_db()  # Ensure database setup before running
    app.run(debug=True)
