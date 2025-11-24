import streamlit as st 
from app.data.db import connect_database
from app.data.datasets import insert_dataset, get_all_datasets, delete_a_dataset

st.title("Dataset Dashboard")
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()

if st.session_state.logged_in:
    conn = connect_database()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Accuracy", "94.2%")
    with col2:
        st.metric("Precision", "91.8%")
    with col3:
        st.metric("Recall", "89.5%")
        
    with st.expander("View All Dataset"):
        dataset = get_all_datasets()
        st.dataframe(dataset, use_container_width = True)

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
    
    if st.button("Log out",type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("Home.py")
        st.stop()
        