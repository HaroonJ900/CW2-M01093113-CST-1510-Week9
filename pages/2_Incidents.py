import streamlit as st
from app.data.db import connect_database 
from app.data.incidents import get_all_incidents, insert_incident, delete_incident, get_incidents_by_severity, get_incidents_by_status, update_incident_status, get_incident_types_with_many_cases, get_incident_by_id
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
st.title("🛡️ Cyber Incidents Dashboard")
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
    if "crime_messages" not in st.session_state:
        st.session_state.crime_messages = [
            {"role":"system","content":"You are a cybersecurity expert. Analyze incidents, threats, and vulnerabilities. Provide technical guidance using MITRE ATT&CK, CVE references. Prioritize actionable recommendation"}
        ]
    
    # ChatGPT interface title and caption
    st.title("💬 ChatGPT - OpenAI API") 
    st.caption("Powered by GPT-4o")

    # display chat messages from session state
    for message in st.session_state.crime_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # take user input and get AI response
    user_input = st.chat_input("Type your message...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
    
        st.session_state.crime_messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages = st.session_state.crime_messages
            )

        ai_response = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(ai_response)

        st.session_state.crime_messages.append({"role": "assistant", "content": ai_response})

    # sidebar controls for chat
    with st.sidebar:
        st.title("⚙️ Crime Incidents Chat Controls")
        count = len(st.session_state.get("crime_messages",[])) - 1
        st.metric("Messages",max(count,0))

        # button to clear chat history
        if st.button("🗑️ Clear Crime Incident Chat", use_container_width=True):
            st.session_state.crime_messages = [
            {"role":"system","content":"You are a cybersecurity expert. Analyze incidents, threats, and vulnerabilities. Provide technical guidance using MITRE ATT&CK, CVE references. Prioritize actionable recommendation"}
        ]
            st.rerun()

    st.divider()
    conn = connect_database()

    # dashboard metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Threats Detected", 247, delta="+12")
    with col2:
        st.metric("Vulnerabilities", 8, delta="-3")
    with col3:
        st.metric("Incidents", 3, delta="+1")

    # view all incidents
    with st.expander("View All Incidents"):
        incidents = get_all_incidents() 
        st.dataframe(incidents, use_container_width=True)

    # add a new incident
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
                
    # fetch incidents by severity
    with st.expander("Get Incident By Severity"):
        with st.form("get_incident_severity"):
            severity = st.selectbox("Severity",["Low","Medium","High","Critical"])
            submitted = st.form_submit_button("Get incident")
            
            if submitted and severity:
                df = get_incidents_by_severity(severity)
                st.dataframe(df)
                st.success("Incident fetched successfully")
                

    # fetch incidents by status
    with st.expander("Get Incident By Status"):
        with st.form("get_incident_status"):
            status = st.selectbox("Status",["Open","In Progress","Resolved"])
            submitted = st.form_submit_button("Get incident")
            if submitted and status:
                df = get_incidents_by_status(status)
                st.dataframe(df)
                st.success("Incident fetched successfully")
                

    # update incident status
    with st.expander("Update Incident Status"):
        with st.form("update_incident_status"):
            incident_id = st.number_input("Incident id",step=1)
            status = st.selectbox("Status",["Open","In Progress","Resolved"])
            submitted = st.form_submit_button("Update Incident")
            if submitted and status:
                update_incident_status(incident_id,status)
                st.success("Incident updated successfully")
                
    # delete an incident
    with st.expander("Delete An Incident"):
        with st.form("Delete Incident"):
              incident_id = st.number_input("Incident id",step=1)
              submitted = st.form_submit_button("Delete incident")

        if submitted and incident_id:
            delete_choice = st.selectbox(f"Are you sure you want to delete ticket #{incident_id}?",["Yes", "No"])
            if delete_choice == "Yes":
                delete_incident(incident_id)
                st.success("Incident Deleted Successful")
                
    # fetch incident types with count greater than a number
    with st.expander("Get Incident by Count"):
        with st.form("Incident_by_count"):
              count = st.number_input("Count",step=1, min_value = 5)
              submitted = st.form_submit_button("Get Incidents")

        if submitted and count:
                df = get_incident_types_with_many_cases(count)
                st.dataframe(df)
                st.success("Incident fetched Successfully")
    
    # analyze a specific incident by ID using ChatGPT
    with st.expander("💬 ChatGPT - Explain Incident By ID Number"):
        incident_id = st.number_input("Enter incident ID",step = 1)
        if st.button("Send Incident Row to ChatGPT"):
            df = get_incident_by_id(incident_id)

            if df.empty:
                st.error("No incident found with that ID")
            else:
                row = df.iloc[0].tolist()
                row_string = str(row)

                message =(f"""
                Analyze this ticket incident based only on these raw values. 
                The columns are: id, title, severity, status, date, user id. 
                The values for this row are: {row_string}.
                """)

                st.session_state.crime_messages.append({"role": "user", "content": message})

                with st.spinner("ChatGPT analyzing the incident..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.crime_messages
                    )

                ai_response = response.choices[0].message.content
                st.session_state.crime_messages.append({"role": "assistant", "content": ai_response})

                st.success("Incident sent to ChatGPT!")
                st.rerun()

    # logout button
    if st.button("Log out",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()
