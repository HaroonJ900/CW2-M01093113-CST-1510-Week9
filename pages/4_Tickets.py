import streamlit as st
from app.data.db import connect_database
from app.data.tickets import insert_ticket, delete_a_ticket, get_all_tickets

st.title("IT Tickets Dashboard")
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()

if st.session_state.logged_in:
    conn = connect_database()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("CPU Usage","67%", delta="+5%")
    with col2:
        st.metric("Memory","8.2 GB", delta="+0.3 GB")
    with col3:
        st.metric("Uptime","99.8%", delta="+0.1%")
        
    with st.expander("View All Tickets"):
        tickets = get_all_tickets()
        st.dataframe(tickets, use_container_width = True)

    with st.expander("Insert a Ticket"):
        with st.form("Add a Ticket"):
            title = st.text_input("Enter title")
            priority = st.selectbox("Priority",["High","Low","Medium","Critical"])
            status = st.selectbox("Status",["Open","In Progress","Resolved"])
            created_date = st.date_input("Select a date")
            user_id = st.number_input("User id",step=1)
            submit = st.form_submit_button("Add Ticket")

            if title and submit:
                insert_ticket(title ,priority ,status ,created_date ,user_id)
                st.success("Ticket add successful")
                st.rerun()

    with st.expander("Delete a ticket"):
        with st.form("Delete a Ticket"):
            ticket_id = st.number_input("ticket id", step=1)
            submit = st.form_submit_button("Delete ticket")

            if ticket_id and submit:
                delete_choice = st.selectbox(f"Are you sure you want to delete ticket #{ticket_id}?",["Yes", "No"])
                if delete_choice == "Yes":
                    delete_a_ticket(ticket_id)
                    st.success("Ticket deleted successfully!")
                    st.rerun()
    
    if st.button("Log out",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()
        