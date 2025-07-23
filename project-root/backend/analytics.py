from backend.db import get_conn

def log_interaction(username, resto_id, action):
    conn = get_conn()
    c = conn.cursor()
    c.execute('INSERT INTO interactions (username, resto_id, action) VALUES (?, ?, ?)',
              (username, resto_id, action))
    conn.commit()
    conn.close()

def get_owner_stats(owner_username):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        SELECT r.restaurant_id, r.name,
            SUM(i.action = "view") as views,
            SUM(i.action = "tap") as taps,
            SUM(i.action = "directions") as directions
        FROM owner_restos o
        JOIN interactions i ON o.resto_id = i.resto_id
        JOIN restaurants r ON o.resto_id = r.restaurant_id
        WHERE o.username = ?
        GROUP BY o.resto_id
    ''', (owner_username,))
    rows = c.fetchall()
    conn.close()
    # Returns: list of (restaurant_id, name, views, taps, directions)
    return rows

def save_owner_resto(username, resto_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('INSERT INTO owner_restos (username, resto_id) VALUES (?, ?)', (username, resto_id))
    conn.commit()
    conn.close()
