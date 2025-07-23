import bcrypt
from backend.db import get_conn

def hash_pw(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_pw(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def signup_user(username, password, display, role):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, hash_pw(password), display, role))
        conn.commit()
        return True, ""
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def login_user(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT password, type, display_name FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and check_pw(password, row[0]):
        return {"username": username, "role": row[1], "display": row[2]}
    return None
