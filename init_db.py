import sqlite3

# Connect to the database (creates 'users.db' if not exists)
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Create users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create passwords table
c.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    site_name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
