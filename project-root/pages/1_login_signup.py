import streamlit as st
from backend.user_auth import signup_user, login_user

st.set_page_config(page_title="Login / Signup")

if 'user_info' not in st.session_state:
    st.session_state["user_info"] = None

if st.session_state.get("logout"):
    st.session_state["user_info"] = None
    st.session_state["logout"] = False

st.title("Login or Signup")

action = st.radio("Choose", ["Login", "Signup"], horizontal=True)
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if action == "Signup":
    display = st.text_input("Display Name")
    role = st.selectbox("User Role", ["user", "admin", "restaurant"])
    if st.button("Sign Up"):
        ok, msg = signup_user(username, password, display, role)
        if ok:
            st.success("Signup successful. You can now log in.")
        else:
            st.error(msg)
else:
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state["user_info"] = user
            st.switch_page("pages/2_recommendations.py")
        else:
            st.error("Invalid credentials")
