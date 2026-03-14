import streamlit as st
import pandas as pd

df = pd.read_csv("dataset/classified_queries.csv")

st.title("AI Customer Support Intelligence Dashboard")

issue_counts = df["category"].value_counts()

st.bar_chart(issue_counts)

percent = (issue_counts / issue_counts.sum()) * 100

st.write("Issue Percentage Distribution")

st.write(percent)
