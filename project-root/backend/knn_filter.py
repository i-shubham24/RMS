from geopy.distance import geodesic

def filter_by_distance(df, center, max_km):
    def dist(row):
        return geodesic(center, (row['latitude'], row['longitude'])).km
    df_copy = df.copy()
    df_copy["distance_km"] = df_copy.apply(dist, axis=1)
    return df_copy[df_copy["distance_km"] <= max_km]
