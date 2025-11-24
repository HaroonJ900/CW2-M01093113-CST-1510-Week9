import streamlit as st
st.title("📊 Dashboard")
if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.username}!")
    if st.button("Incidents"):
        st.switch_page("pages/2_Incidents.py")
    if st.button("Datasets"):
        st.switch_page("pages/3_Datasets.py")
    if st.button("Tickets"):
        st.switch_page("pages/4_Tickets.py")   
    if st.button("Analytics"):
        st.switch_page("pages/5_Analytics.py")
    if st.button("Settings"):
        st.switch_page("pages/6_Settings.py")
    if st.button("Log out",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()   
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()