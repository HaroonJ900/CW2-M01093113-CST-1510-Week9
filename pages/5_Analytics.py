import streamlit as st
from app.data.db import connect_database
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_datasets
from app.data.incidents import get_all_incidents
import plotly.express as px

st.title("Analytics Dashboard")
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to home page."):
        st.switch_page("Home.py")
        st.stop()

if st.session_state.logged_in:
    st.header("1. Cyber Incidents Graph")
    df1 = get_all_incidents()
    crime_count_df = df1.groupby("title").size().reset_index() 
    crime_count_df.columns = ["title","count"]
    chart = px.pie(
        crime_count_df,
        names="title",
        values="count",
        title = "Crime Distribution"
    )
    st.plotly_chart(chart)

    st.header("2. Datasets Graphs")
    df2 = get_all_datasets()
    dataset_count = df2.groupby("name").size()
    st.write("### Each Type Dataset Count")
    st.bar_chart(dataset_count)
    size_count = df2.groupby("size").size()
    st.write("### Number of Counts Per Size")
    st.line_chart(size_count)
    
    st.header("3. Ticket Graphs")
    df3 = get_all_tickets()
    title_count = df3.groupby("title").size()
    st.write("### Each Type Ticket Count")
    st.bar_chart(title_count)
    status_count = df3.groupby("status").size()
    st.write("### Count by Status")
    st.bar_chart(status_count)
