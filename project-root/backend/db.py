import sqlite3

def get_conn():
    return sqlite3.connect("data/users.db", check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        display_name TEXT,
        type TEXT
    )''')
    conn.commit()
    conn.close()
