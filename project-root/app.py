import streamlit as st

<<<<<<< HEAD
# Define all app pages with custom labels and icons
pages = [
    st.Page("home.py", title="Home", icon="🏠"),
    st.Page("pages/1_login_signup.py", title="Login & Signup", icon="🔐"),
    st.Page("pages/2_recommendations.py", title="Recommendations", icon="🍽️"),
    st.Page("pages/3_restaurant_dashboard.py", title="Restaurant Dashboard", icon="📊"),
    st.Page("pages/4_user_dashboard.py", title="User Dashboard", icon="👤"),
]

# Optional: Add a global page title for browser tab
st.set_page_config(page_title="Punjab Restaurant Recommender")

# Display sidebar navigation for all app pages
pg = st.navigation(pages, position="sidebar")
pg.run()
=======
st.set_page_config(page_title="Restaurant App", page_icon="🍽️")
st.title("Welcome to Punjab Restaurant Recommender")

st.info("➡️ Use the sidebar to Login/Signup and explore restaurants.")
>>>>>>> 528974486cdc99b3f303d412ebb3f9fefd49a26c
