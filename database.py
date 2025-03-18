import sqlite3

# Connect to database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create passwords table with correct schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        site_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()
