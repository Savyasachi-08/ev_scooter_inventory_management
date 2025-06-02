import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )''')

    # Create vehicles table
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id TEXT UNIQUE NOT NULL,
        model_name TEXT,
        manufacture_date TEXT,
        battery_capacity TEXT,
        motor_power TEXT,
        color TEXT,
        notes TEXT
    )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
