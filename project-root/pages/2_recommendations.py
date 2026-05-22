import streamlit as st
from streamlit_folium import st_folium
from streamlit.components.v1 import html
from backend.data_loader import load_data
from backend.knn_filter import filter_by_distance
from frontend.google_maps import create_map
import pandas as pd

def recommendations():
    st.title("Recommendations")
    st.write("Restaurant recommendations will be shown here.")

if __name__ == "__page__":
    recommendations()


# -------------------- Config --------------------
# Remove padding and vertical gaps below map
st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem !important; }
    .main { padding-bottom: 0px !important; }
    iframe, .folium-map { margin: 0 !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# -------------------- Auth Check --------------------
if "user_info" not in st.session_state or not st.session_state["user_info"]:
    st.switch_page("pages/1_login_signup.py")

if st.sidebar.button("Log Out"):
    st.session_state["user_info"] = None
    st.switch_page("pages/1_login_signup.py")

# -------------------- Location Handling --------------------
DEFAULT_LAT, DEFAULT_LON = 31.6340, 74.8723
def safe_latlon(lat, lon):
    try:
        return float(lat), float(lon)
    except:
        return DEFAULT_LAT, DEFAULT_LON

if "current_loc" not in st.session_state:
    st.session_state["current_loc"] = (DEFAULT_LAT, DEFAULT_LON)
user_lat, user_lon = safe_latlon(*st.session_state["current_loc"])

# -------------------- Sidebar Filters --------------------
st.sidebar.title("Filters")
distance_km = st.sidebar.slider("Search Distance (km)", 1, 20, 5)
min_rating, max_rating = st.sidebar.slider("Rating Range", 2.0, 5.0, (3.5, 5.0), 0.1)

df = load_data()

# Cleanup
df = df[pd.to_numeric(df["latitude"], errors="coerce").notnull()]
df = df[pd.to_numeric(df["longitude"], errors="coerce").notnull()]
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

df["cuisine"] = df["cuisine"].fillna("Unknown")
df["veg_nonveg"] = df["veg_nonveg"].fillna("Unknown")

# Cuisine + Type Filter
all_cuisines = sorted({c.strip() for x in df["cuisine"] for c in str(x).split("|")})
selected_cuisines = st.sidebar.multiselect("Cuisines", all_cuisines, default=all_cuisines)
veg_options = ["Any"] + sorted(df["veg_nonveg"].dropna().unique())
veg = st.sidebar.selectbox("Veg/Non-Veg", veg_options)

# -------------------- Data Filter --------------------
df = filter_by_distance(df, (user_lat, user_lon), distance_km)
df = df[df["rating"].between(min_rating, max_rating)]

if selected_cuisines:
    df = df[df["cuisine"].apply(lambda x: any(c.lower() in str(x).lower() for c in selected_cuisines))]

if veg != "Any":
    df = df[df["veg_nonveg"] == veg]

# -------------------- Map --------------------
user_lat, user_lon = safe_latlon(user_lat, user_lon)
fmap = create_map(user_lat, user_lon, df, distance_km)

map_result = st_folium(
    fmap,
    height=360,
    use_container_width=True,
    returned_objects=["last_clicked"]
)

# Reduce space between map and cards
st.markdown("<div style='margin-top: -60px'></div>", unsafe_allow_html=True)

# Tap to recenter
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
        st.markdown(f"**Cuisine:** {row['cuisine']}  \n"
                f"**Veg/Non-Veg:** {row['veg_nonveg']}  \n"
                f"**Rating:** {row['rating']} ★  \n"
                f"**Distance:** {row['distance_km']:.2f} km")
    with col2:
        route_url = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{row['latitude']},{row['longitude']}/"
        st.link_button("Route", route_url)
    st.markdown("---")

st.sidebar.caption(f"📍 Current Location: {user_lat:.4f}, {user_lon:.4f}")
