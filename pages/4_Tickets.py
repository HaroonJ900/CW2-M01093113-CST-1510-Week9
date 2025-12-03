import streamlit as st
from app.data.db import connect_database
from app.data.tickets import insert_ticket, delete_a_ticket, get_all_tickets, get_ticket_by_id
from openai import OpenAI

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
st.title("🎫 IT Tickets Dashboard")
st.divider()

# redirect if user is not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()

if st.session_state.logged_in:
    # initialize OpenAI client
    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

    # initialize chat history if it does not exist
    if "ticket_messages" not in st.session_state:
        st.session_state.ticket_messages = [
            {"role":"system","content":"You are an IT operations expert. Help troubleshoot issues, optimize systems, manage tickets, and provide infrastructure guidance. Focus on practical solutions"}
        ]
    st.title("💬 ChatGPT - OpenAI API") 
    st.caption("Powered by GPT-4o-mini")  

    # display chat messages from session state
    for message in st.session_state.ticket_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # take user input and get AI response
    user_input = st.chat_input("Type your message....")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.ticket_messages.append({"role":"user","content":user_input})
        with st.spinner("Thinking...."):
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = st.session_state.ticket_messages
            )
        
        ai_response = response.choices[0].message.content 

        with st.chat_message("assistant"):
            st.write(ai_response)
        
        st.session_state.ticket_messages.append({"role":"assistant","content":ai_response})

    # sidebar controls for ticket chat
    with st.sidebar:
        st.title("⚙️ Ticket Chat Controls")

        count = len(st.session_state.get("ticket_messages",[])) -1
        st.metric("Messages",max(count,0))

        # button to clear chat history
        if st.button("🗑️ Clear Ticket Chat", use_container_width=True):
            st.session_state.ticket_messages = [
            {"role": "system", "content": "You are an IT operations expert. Help troubleshoot issues, optimize systems, manage tickets, and provide infrastructure guidance. Focus on practical solutions"}
            ]
            st.rerun()

    st.divider()
    conn = connect_database()

    # dashboard metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPU Usage","67%", delta="+5%")
    with col2:
        st.metric("Memory","8.2 GB", delta="+0.3 GB")
    with col3:
        st.metric("Uptime","99.8%", delta="+0.1%")
        
    # view all tickets
    with st.expander("View All Tickets"):
        tickets = get_all_tickets()
        st.dataframe(tickets, use_container_width = True)

    # insert a new ticket
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

    # delete a ticket
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
    
    # send a specific ticket row to ChatGPT for explanation
    with st.expander("💬 ChatGPT - Explain Ticket By ID Number"):
        ticket_id = st.number_input("Enter Ticket ID",step = 1)
        if st.button("Send Ticket Row to ChatGPT"):
            df = get_ticket_by_id(ticket_id)

            if df.empty:
                st.error("No ticket found with that ID")
            else:
                row = df.iloc[0].tolist()
                row_string = str(row)

                message =(f"""
            Only describe the data in this row. Do not provide any analysis, interpretation, or recommendations.
            Analyze this dataset of ticket incidents based solely on the values in this row.
            The columns are: id, title, priority, status, created date, user id.
            The values for this row are: {row_string}.
            """)

                st.session_state.ticket_messages.append({"role": "user", "content": message})

                with st.spinner("ChatGPT analyzing the ticket..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.ticket_messages
                    )

                ai_response = response.choices[0].message.content
                st.session_state.ticket_messages.append({"role": "assistant", "content": ai_response})

                st.success("Incident sent to ChatGPT!")
                st.rerun()
    
    # logout button
    if st.button("Log out",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()
