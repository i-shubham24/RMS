import streamlit as st
import pandas as pd
import os

def user_dashboard():
    st.title("User Dashboard")
    st.write("Dashboard with user profile and saved restaurants.")

if __name__ == "__page__":
    user_dashboard()


LOG_PATH = "data/user_events.csv"

if "user_info" not in st.session_state or not st.session_state["user_info"]:
    st.switch_page("pages/1_login_signup.py")

user = st.session_state["user_info"]
if user["role"] != "user":
    st.error("Only user accounts can view this dashboard.")
    st.stop()

st.title("📊 User Activity Dashboard")

if not os.path.exists(LOG_PATH):
    st.info("No activity yet.")
    st.stop()

df = pd.read_csv(LOG_PATH)
df = df[df["username"] == user["username"]].sort_values("timestamp", ascending=False)

if df.empty:
    st.info("No recorded activity.")
else:
    with st.expander("🔍 Search History"):
        st.dataframe(df[df["event_type"] == "search"][["timestamp", "details"]])

    with st.expander("👁️ Viewed Restaurants"):
        st.dataframe(df[df["event_type"] == "view"][["timestamp", "details"]])

    with st.expander("📍 Routes Clicked"):
        st.dataframe(df[df["event_type"] == "route"][["timestamp", "details"]])
