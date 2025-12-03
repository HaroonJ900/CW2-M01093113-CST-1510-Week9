import streamlit as st
from app.data.auth import login_user, register_user, user_exist

# set background image for the page
image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/1287145/pexels-photo-1287145.jpeg?cs=srgb&dl=pexels-eberhardgross-1287145.jpg&fm=jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
"""

st.markdown(image, unsafe_allow_html=True)
# sets page title, icon, and layout
st.set_page_config(page_title="Login / Register", page_icon ="🔑",
layout = "centered")

# initialize session state variables for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Welcome")

# show message if already logged in
if st.session_state.logged_in:
    st.success(f"Already logged in as **{ st.session_state.username}**")
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

# create two tabs: Login and Register
tab_login, tab_register = st.tabs(["Login", "Register"])

# Login Tab
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        try:
            # verify login credentials
            if login_user(login_username ,login_password):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success(f"Welcome back, {login_username}! 🎉 ")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Register Tab
with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    role = st.text_input("Enter role user/admin")
    if st.button("Create account", key="create_account"):
        try:
            # validation checks before registration
            if not new_username or not new_password:
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif user_exist(new_username):
                st.error("Username already exists")
            else:
                # register the new user
                register_user(new_username, new_password,role)
                st.success("Account created successfully")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
