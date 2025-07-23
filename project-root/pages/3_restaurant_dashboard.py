import streamlit as st
from streamlit_folium import st_folium
from backend.data_loader import load_data
from backend.knn_filter import filter_by_distance
from frontend.google_maps import create_map
from utils.logger import log_event
import pandas as pd

# -------------------- Page Config --------------------
st.set_page_config(page_title="Restaurant Recommendations", layout="wide")

# Minimize whitespace below map and top header
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem !important;
    }
    .main {
        padding-bottom: 0px !important;
    }
    iframe, .folium-map {
        margin: 0 !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- Session/Auth Check --------------------
if "user_info" not in st.session_state or not st.session_state["user_info"]:
    st.switch_page("pages/1_login_signup.py")

user = st.session_state["user_info"]
username = user["username"]

if st.sidebar.button("Log Out"):
    st.session_state["logout"] = True
    st.session_state["user_info"] = None
    st.switch_page("pages/1_login_signup.py")

# -------------------- Location --------------------
DEFAULT_LAT, DEFAULT_LON = 31.6340, 74.8723

def safe_latlon(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        if lat is None or lon is None:
            raise ValueError
        return lat, lon
    except:
        return DEFAULT_LAT, DEFAULT_LON

if "current_loc" not in st.session_state:
    st.session_state["current_loc"] = (DEFAULT_LAT, DEFAULT_LON)

user_lat, user_lon = safe_latlon(*st.session_state["current_loc"])

# -------------------- Sidebar Filters --------------------
st.sidebar.title("Filters")
distance_km = st.sidebar.slider("Search Radius (km)", 1, 20, 5)
min_rating, max_rating = st.sidebar.slider("Rating Range", 2.0, 5.0, (3.5, 5.0), 0.1)

df = load_data()

# Cleanup
df = df[pd.to_numeric(df["latitude"], errors="coerce").notnull()]
df = df[pd.to_numeric(df["longitude"], errors="coerce").notnull()]
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

df["cuisine"] = df["cuisine"].fillna("Unknown")
df["veg_nonveg"] = df["veg_nonveg"].fillna("Unknown")

# Sidebar cuisine + dietary filters
all_cuisines = sorted({c.strip() for row in df["cuisine"] for c in str(row).split("|")})
selected_cuisines = st.sidebar.multiselect("Cuisines", all_cuisines, default=all_cuisines)

veg_types = ["Any"] + sorted(df["veg_nonveg"].dropna().unique())
veg = st.sidebar.selectbox("Veg/Non-Veg", veg_types)

# -------------------- Log Search --------------------
if user["role"] == "user":
    filters = f"distance={distance_km}km, rating={min_rating}-{max_rating}, cuisine={selected_cuisines}, veg={veg}"
    log_event(username, "search", filters)

# -------------------- Filter Data --------------------
df = filter_by_distance(df, (user_lat, user_lon), distance_km)
df = df[df["rating"].between(min_rating, max_rating)]

if selected_cuisines:
    df = df[df["cuisine"].apply(lambda x: any(c.lower() in str(x).lower() for c in selected_cuisines))]

if veg != "Any":
    df = df[df["veg_nonveg"] == veg]

# -------------------- Create Map --------------------
user_lat, user_lon = safe_latlon(user_lat, user_lon)
fmap = create_map(user_lat, user_lon, df, distance_km)

map_result = st_folium(
    fmap,
    height=360,
    use_container_width=True,
    returned_objects=["last_clicked"]
)

# -------------------- Tighten layout below map --------------------
st.markdown("<div style='margin-top: -60px'></div>", unsafe_allow_html=True)

# -------------------- Tap-to-Set Location --------------------
if map_result and map_result.get("last_clicked"):
    lat = map_result["last_clicked"]["lat"]
    lon = map_result["last_clicked"]["lng"]
    st.session_state["current_loc"] = safe_latlon(lat, lon)
    st.rerun()

# -------------------- Results --------------------
st.markdown(f"### {len(df)} restaurants found")

for _, row in df.iterrows():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(row["name"])
        st.markdown(f"Cuisine: {row['cuisine']}")
        st.markdown(f"Rating: {row['rating']} ★")
        # ✅ Log view
        if user["role"] == "user":
            log_event(username, "view", row["name"])
    with col2:
        route_url = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{row['latitude']},{row['longitude']}/"
        if st.link_button("Route", route_url):
            log_event(username, "route", row["name"])
    st.markdown("---")

# -------------------- User Display Hint --------------------
st.sidebar.caption(f"📍 Your Location: {user_lat:.4f}, {user_lon:.4f}")
