import streamlit as st

# sets a custom background color for the Streamlit app
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

st.title("📊 Dashboard")
st.divider()

# shows the dashboard only if the user is logged in
if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.username}!")

    # button to open the incidents page
    if st.button("🛡️ Incidents"):
        st.switch_page("pages/2_Incidents.py")

    # button to open the datasets page
    if st.button("📁 Datasets "):
        st.switch_page("pages/3_Datasets.py")

    # button to open the tickets page
    if st.button("🎫 Tickets "):
        st.switch_page("pages/4_Tickets.py")   

    # button to open analytics dashboard
    if st.button("📈 Analytics"):
        st.switch_page("pages/5_Analytics.py")

    # button to open settings page
    if st.button("⚙️ Settings "):
        st.switch_page("pages/6_Settings.py")

    # handles logout and sends user back to home
    if st.button(" Log out ",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()   

# message shown when someone tries to access dashboard without logging in
if not st.session_state.logged_in:
        st.error("You must be logged in to view the dashboard.")
        if st.button("Go to home page."):
            st.switch_page("Home.py")
            st.stop()
