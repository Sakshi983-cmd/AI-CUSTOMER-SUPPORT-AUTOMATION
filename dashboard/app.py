import streamlit as st
import pandas as pd

df = pd.read_csv("../dataset/customer_queries.csv")

def classify(q):
    q=q.lower()
    if "refund" in q:
        return "Refund"
    elif "payment" in q:
        return "Payment Issue"
    elif "delivery" in q or "order" in q:
        return "Order / Delivery"
    elif "product" in q:
        return "Product Complaint"
    else:
        return "General"

df["category"]=df["query"].apply(classify)

st.title("AI Customer Support Dashboard")

issue_counts=df["category"].value_counts()

st.bar_chart(issue_counts)

st.write(issue_counts)
