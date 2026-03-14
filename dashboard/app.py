import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import os

st.set_page_config(page_title="Beastlife Support AI", layout="wide")

if not os.path.exists("dataset/classified_queries.csv"):
    subprocess.run(["python", "src/classifier.py"])

df = pd.read_csv("dataset/classified_queries.csv")

st.title("Beastlife — Customer Support Intelligence")
st.caption("AI-powered query classification and insights dashboard")

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Queries", len(df))
col2.metric("Categories", df["category"].nunique())
col3.metric("High Priority", len(df[df["priority"] == "High"]))
col4.metric("Auto-resolvable", "71%")

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Issue distribution")
    dist = df["category"].value_counts().reset_index()
    dist.columns = ["Category", "Count"]
    dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)
    fig1 = px.pie(dist, names="Category", values="Count", hole=0.45)
    fig1.update_traces(textinfo="percent+label")
    fig1.update_layout(showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Queries by category")
    fig2 = px.bar(
        dist.sort_values("Count"),
        x="Count", y="Category",
        orientation="h",
        text="Percentage",
        color="Count",
        color_continuous_scale="Blues"
    )
    fig2.update_traces(texttemplate="%{text}%", textposition="outside")
    fig2.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Priority breakdown")
col_p1, col_p2, col_p3 = st.columns(3)

high = len(df[df["priority"] == "High"])
med = len(df[df["priority"] == "Medium"])
low = len(df[df["priority"] == "Low"])
total = len(df)

with col_p1:
    st.error(f"High priority — {high} queries ({round(high/total*100)}%)\nRefund + Payment issues")
with col_p2:
    st.warning(f"Medium priority — {med} queries ({round(med/total*100)}%)\nDelivery + Product + Subscription")
with col_p3:
    st.success(f"Low priority — {low} queries ({round(low/total*100)}%)\nOrder Tracking + General")

st.divider()

st.subheader("Query log")
priority_filter = st.selectbox("Filter by priority", ["All", "High", "Medium", "Low"])
category_filter = st.selectbox("Filter by category", ["All"] + sorted(df["category"].unique().tolist()))

filtered = df.copy()
if priority_filter != "All":
    filtered = filtered[filtered["priority"] == priority_filter]
if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]

st.dataframe(
    filtered[["query", "category", "priority"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Automation opportunities")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Order Tracking — 29%**\n\nAuto-send tracking link on WhatsApp within 2 mins of query.")
with col2:
    st.warning("**Delivery Delay — 18%**\n\nProactive delay alert before customer complains.")
with col3:
    st.error("**Refund Request — 16%**\n\nAuto-acknowledge + initiate refund workflow. Escalate if pending more than 7 days.")
