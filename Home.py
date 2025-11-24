import streamlit as st
from app.data.auth import login_user, register_user, user_exist

st.set_page_config(page_title="Login / Register", page_icon ="🔑",
layout = "centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔐 Welcome")

if st.session_state.logged_in:
    st.success(f"Already logged in as **{ st.session_state.username}**")
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        try:
            if login_user(login_username ,login_password):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.success(f"Welcome back, {login_username}! 🎉 ")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    if st.button("Create account", key="create_account"):
        try:
            if not new_username or not new_password:
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif user_exist(new_username):
                st.error("Username already exists")
            else:
                register_user(new_username, new_password)
                st.success("Account created successfully")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
