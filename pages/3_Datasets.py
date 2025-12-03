import streamlit as st 
from app.data.db import connect_database
from app.data.datasets import insert_dataset, get_all_datasets, delete_a_dataset, get_dataset_by_id
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
st.title("📁 Dataset Dashboard")
st.divider()

# redirect if user is not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()

if st.session_state.logged_in:
    # initialize OpenAI client
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # initialize chat history if it does not exist
    if "ds_messages" not in st.session_state:
        st.session_state.ds_messages = [
            {"role":"system","content":"You are a data science expert. Help with data analysis, visualization, statistical methods, and machine learning. Explain concepts clearly and suggest appropriate techniques"}
        ]
    
    # ChatGPT interface title and caption
    st.title("💬 ChatGPT - OpenAI API") 
    st.caption("Powered by GPT-4o-mini")

    # display chat messages from session state
    for message in st.session_state.ds_messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # take user input and get AI response
    user_input = st.chat_input("Type your message...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.ds_messages.append({"role":"user","content":user_input})
        with st.spinner("Thinking...."):
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = st.session_state.ds_messages
            )

        ai_response = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(ai_response)

        st.session_state.ds_messages.append({"role":"assistant","content":ai_response})

    # sidebar controls for data science chat
    with st.sidebar:
        st.title("⚙️ Data Science Chat Controls")
        count = len(st.session_state.get("ds_messages", [])) - 1
        st.metric("Messages", max(count, 0))

        # button to clear chat history
        if st.button("🗑️ Clear DS Chat", use_container_width=True):
            st.session_state.ds_messages = [
            {"role": "system", "content": "You are a data science expert. Help with data analysis, visualization, statistical methods, and machine learning. Explain concepts clearly and suggest appropriate techniques"}
            ]
            st.rerun()

    st.divider()
    conn = connect_database()

    # dashboard metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accuracy", "94.2%")
    with col2:
        st.metric("Precision", "91.8%")
    with col3:
        st.metric("Recall", "89.5%")
        
    # view all datasets
    with st.expander("View All Dataset"):
        dataset = get_all_datasets()
        st.dataframe(dataset, use_container_width = True)

    # insert a new dataset
    with st.expander("Insert a Dataset"):
        with st.form("Add a Dataset"):
            name = st.text_input("Enter name")
            source = st.text_input("Enter source")
            category = st.text_input("Enter category")
            size = st.text_input("Enter the size in mb ")
            submit = st.form_submit_button("Add dataset")

            if name and submit:
                insert_dataset(name, source, category, size)
                st.success("Dataset add successful")
                st.rerun()

    # delete a dataset
    with st.expander("Delete a Dataset"):
        with st.form("Delete a Dataset"):
            dataset_id = st.number_input("Dataset id", step=1)
            submit = st.form_submit_button("Delete dataset")

        if dataset_id and submit:
            delete_choice = st.selectbox(f"Are you sure you want to delete dataset #{dataset_id}?",["Yes", "No"])
            if delete_choice == "Yes":
                delete_a_dataset(dataset_id)
                st.success("Dataset delete successful")
                st.rerun()

    # send a specific dataset row to ChatGPT for explanation
    with st.expander("💬 ChatGPT - Explain Dataset By ID Number"):
        dataset_id = st.number_input("Enter Dataset ID",step = 1)
        if st.button("Send Incident Row to ChatGPT"):
            df = get_dataset_by_id(dataset_id)

            if df.empty:
                st.error("No Dataset found with that ID")
            else:
                row = df.iloc[0].tolist()
                row_string = str(row)

                message =(f"""Only describe the data in this row. Do not provide any analysis, interpretation, or recommendations.
                Analyze this dataset of log files based solely on the values in this row.
                The columns are: id, name, source, category, size.
                The values for this row are: {row_string}.""")

                st.session_state.ds_messages.append({"role": "user", "content": message})

                with st.spinner("ChatGPT analyzing the dataset..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.ds_messages
                    )

                ai_response = response.choices[0].message.content
                st.session_state.ds_messages.append({"role": "assistant", "content": ai_response})

                st.success("Incident sent to ChatGPT!")
                st.rerun()

    # logout button
    if st.button("Log out",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()