import folium

def get_color(rating):
    try:
        rating = float(rating)
    except:
        return 'gray'
    if rating >= 4.5: return 'green'
    if rating >= 4.0: return 'lightgreen'
    if rating >= 3.5: return 'orange'
    if rating >= 3.0: return 'lightred'
    return 'red'

def create_map(user_lat, user_lon, df_filtered, distance_km):
    try:
        user_lat = float(user_lat)
        user_lon = float(user_lon)
        if user_lat is None or user_lon is None:
            raise ValueError
    except:
        user_lat, user_lon = 31.6340, 74.8723

    fmap = folium.Map(location=[user_lat, user_lon], zoom_start=13)

    # Draw radius
    folium.Circle(
        [user_lat, user_lon],
        radius=distance_km * 1000,
        color="blue",
        fill=True,
        fill_opacity=0.1
    ).add_to(fmap)

    # Add center marker
    folium.Marker(
        [user_lat, user_lon],
        tooltip="Current Location",
        icon=folium.Icon(color="blue")
    ).add_to(fmap)

    # Add restaurant markers
    for _, row in df_filtered.iterrows():
        try:
            lat, lon = float(row["latitude"]), float(row["longitude"])
            rating = float(row.get("rating", 0))
            url = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{lat},{lon}/"
            popup = folium.Popup(
                f"<b>{row['name']}</b><br>{row['cuisine']}<br>{row.get('veg_nonveg', '')}<br>"
                f"Rating: {rating} ★<br><a href='{url}' target='_blank'>Route</a>",
                max_width=250
            )
            marker_color = get_color(rating)
            folium.Marker(
                [lat, lon],
                tooltip=f"{row['name']} ({rating}★)",
                popup=popup,
                icon=folium.Icon(color=marker_color)
            ).add_to(fmap)
        except:
            continue

    return fmap
