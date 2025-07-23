import streamlit as st
import pandas as pd
import os

DATA_PATH = "data/restaurants.csv"

st.set_page_config(page_title="Restaurant Dashboard", layout="wide")

# Permissions
if "user_info" not in st.session_state or not st.session_state["user_info"]:
    st.switch_page("pages/1_login_signup.py")

user = st.session_state["user_info"]
if user["role"] != "restaurant":
    st.error("Access Denied: Only restaurant accounts allowed.")
    st.stop()

if st.sidebar.button("Log Out"):
    st.session_state["user_info"] = None
    st.switch_page("pages/1_login_signup.py")

st.title("Restaurant Dashboard")
st.subheader("➕ Add a New Restaurant")

with st.form("add_restaurant_form"):
    name = st.text_input("Restaurant Name")
    state = st.text_input("State")
    district = st.text_input("District")
    lat = st.text_input("Latitude")
    lon = st.text_input("Longitude")
    cuisine = st.text_input("Cuisines (e.g. Indian|Chinese|Pizza)")
    veg_nonveg = st.selectbox("Type", ["Veg", "Non-Veg", "Both"])
    rating = st.slider("Rating", 1.0, 5.0, 4.2, 0.1)
    image_path = st.text_input("Image URL or local path")

    submitted = st.form_submit_button("Add Restaurant")

    if submitted:
        try:
            lat = float(lat)
            lon = float(lon)

            if not name or not cuisine:
                st.error("Name and Cuisine are required!")
            else:
                if not os.path.exists(DATA_PATH):
                    df = pd.DataFrame(columns=[
                        "restaurant_id", "name", "state", "district", "latitude", "longitude",
                        "cuisine", "veg_nonveg", "image_path", "rating"
                    ])
                else:
                    df = pd.read_csv(DATA_PATH)

                rest_id = f"{user['username']}_{len(df)+1}"
                new_row = pd.DataFrame([{
                    "restaurant_id": rest_id,
                    "name": name,
                    "state": state,
                    "district": district,
                    "latitude": lat,
                    "longitude": lon,
                    "cuisine": cuisine,
                    "veg_nonveg": veg_nonveg,
                    "image_path": image_path,
                    "rating": rating
                }])

                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_PATH, index=False)

                st.success("✅ Restaurant added.")
        except:
            st.error("Invalid latitude or longitude.")
