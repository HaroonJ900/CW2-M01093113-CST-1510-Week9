import streamlit as st
from app.data.auth import hash_password
from app.data.db import connect_database

USER_DATA_FILE = "users.txt"

# set custom background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F6F5F4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("⚙️ Settings")
st.divider()

# redirect if user is not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view settings.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()

if st.session_state.logged_in:
    # Change password section
    with st.expander("Change Password"):
        new_password = st.text_input("Enter your new password.", type="password")
        if st.button("Change Password"):
            username = st.session_state.username
            hashed_password = hash_password(new_password)

            # Update password in the database
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (hashed_password, username)
            )
            conn.commit()
            conn.close()

            st.success("Password updated successfully!")
