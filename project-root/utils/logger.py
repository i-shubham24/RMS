import pandas as pd
import os
from datetime import datetime

LOG_PATH = "data/user_events.csv"

def log_event(username, event_type, details):
    if not os.path.exists(LOG_PATH):
        df = pd.DataFrame(columns=["username", "timestamp", "event_type", "details"])
    else:
        df = pd.read_csv(LOG_PATH)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.concat([df, pd.DataFrame([{
        "username": username,
        "timestamp": ts,
        "event_type": event_type,
        "details": details
    }])], ignore_index=True)

    df.to_csv(LOG_PATH, index=False)
