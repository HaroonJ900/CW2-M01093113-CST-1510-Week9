import streamlit as st
from app.data.db import connect_database 
from app.data.incidents import get_all_incidents, insert_incident, delete_incident

st.title("Cyber Incidents Dashboard")
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()

if st.session_state.logged_in:
    conn = connect_database()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Threats Detected", 247, delta="+12")
    with col2:
        st.metric("Vulnerabilities", 8, delta="-3")
    with col3:
        st.metric("Incidents", 3, delta="+1")

    with st.expander("View All Incidents"):
        incidents = get_all_incidents() 
        st.dataframe(incidents, use_container_width=True)

    with st.expander("Add New Incident"):
        with st.form("new_incident"):
            title = st.text_input("Incidents title")
            severity = st.selectbox("Severity",["Low","Medium","High","Critical"])
            status = st.selectbox("Status",["Open","In Progress","Resolved"])
            date = st.date_input("Select a date")
            user_id = st.number_input("User id",step=1)
            submitted = st.form_submit_button("Add incident")

            if submitted and title:
                insert_incident(date,title,severity,status,user_id)
                st.success("Incident added successful")
                st.rerun()
    with st.expander("Delete An Incident"):
        with st.form("Delete Incident"):
              incident_id = st.number_input("Incident id",step=1)
              submitted = st.form_submit_button("Delete incident")

        if submitted and incident_id:
            delete_choice = st.selectbox(f"Are you sure you want to delete ticket #{incident_id}?",["Yes", "No"])
            if delete_choice == "Yes":
                delete_incident(incident_id)
                st.success("Incident Deleted Successful")
                st.rerun()
    if st.button("Log out",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()




