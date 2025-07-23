import pandas as pd
import os

def load_data():
    path = "data/restaurants.csv"
    if not os.path.exists(path):
        df = pd.DataFrame(columns=[
            "restaurant_id", "name", "state", "district",
            "latitude", "longitude", "cuisine",
            "veg_nonveg", "image_path", "rating"
        ])
        df.to_csv(path, index=False)
    return pd.read_csv(path)
