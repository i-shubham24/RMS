import sqlite3
import os

def get_conn():
    # 1. Get the absolute path of your project root (assuming db.py is in /backend)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 2. Define the path to the data folder
    data_dir = os.path.join(base_dir, "data")
    
    # 3. Create the data directory if it doesn't exist on the Streamlit server
    os.makedirs(data_dir, exist_ok=True)
    
    # 4. Connect to the database
    db_path = os.path.join(data_dir, "users.db")
    return sqlite3.connect(db_path, check_same_thread=False)