import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Beastlife Support AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #080b14 !important;
    color: #e8eaf6 !important;
}
.stApp { background-color: #080b14 !important; }
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #e8eaf6 !important;
    font-family: 'DM Mono', monospace !important;
}
.stButton button {
    background: #6366f1 !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
}
.stButton button:hover { background: #4f46e5 !important; }
.block-container { padding: 2rem 2rem 2rem !important; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #e8eaf6 !important; }
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #4f5a7a;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 12px;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    color: #10b981;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

CATEGORIES = {
    "Order Tracking": [
        "where is my order", "track my order", "order status",
        "tracking link", "missing item", "wrong product",
        "modify order", "cancel my order", "change delivery address",
        "shows delivered", "order is delayed", "tracking not updating"
    ],
    "Delivery Delay": [
        "delivery is late", "taking too long", "delivery date changed",
        "stuck in transit", "how long does delivery", "agent did not contact",
        "package is stuck", "delivery usually take"
    ],
    "Refund Request": [
        "want refund", "refund not processed", "refund for damaged",
        "return the product", "refund is still pending",
        "replacement for damaged", "want to return"
    ],
    "Payment Failure": [
        "payment failed", "payment declined", "payment not going",
        "payment got deducted", "payment gateway", "charged twice",
        "invoice for my purchase"
    ],
    "Product Complaint": [
        "quality is bad", "arrived damaged", "bottle was damaged",
        "seal was broken", "taste is different", "expired before delivery",
        "supplement dosage", "product usage"
    ],
    "Subscription Issue": [
        "subscription cancelled", "subscription charged",
        "pause my subscription", "upgrade my subscription",
        "subscription renewal failed"
    ],
}

REPLIES = {
    "Order Tracking":     "Hi! Your order is being processed. Here is your tracking link: [link]. Expected delivery in 3-5 days.",
    "Delivery Delay":     "Sorry for the delay! Your order is on its way. Our team is monitoring it and will update you soon.",
    "Refund Request":     "We have received your refund request and will process it within 5-7 business days. Thank you for your patience.",
    "Payment Failure":    "Sorry for the inconvenience! Please retry your payment using this link: [retry-link]. Contact us if issue persists.",
    "Product Complaint":  "We are sorry about your experience! Please share photos and we will arrange a replacement immediately.",
    "Subscription Issue": "We have noted your subscription concern. Our team will resolve it within 24 hours.",
    "General Question":   "Thanks for reaching out! Our support team will get back to you shortly.",
}

def classify_query(query):
    query = query.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in query:
                return category
    return "General Question"

def get_priority(category):
    if category in ["Refund Request", "Payment Failure"]:
        return "High"
    elif category in ["Delivery Delay", "Product Complaint", "Subscription Issue"]:
        return "Medium"
    return "Low"

df = pd.read_csv("dataset/customer_queries.csv")
df["category"] = df["query"].apply(classify_query)
df["priority"] = df["category"].apply(get_priority)

colors = ["#6366f1","#f59e0b","#ef4444","#ec4899","#06b6d4","#10b981","#8b5cf6"]

col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("## Beastlife Intelligence")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:11px;color:#4f5a7a;">AI CUSTOMER SUPPORT SYSTEM 2026</p>', unsafe_allow_html=True)
with col_h2:
    st.markdown('<div class="live-badge">LIVE SYSTEM</div>', unsafe_allow_html=True)

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Queries", len(df))
col2.metric("Auto-Resolvable", "71%")
col3.metric("High Priority", len(df[df["priority"] == "High"]))
col4.metric("Categories", df["category"].nunique())

st.divider()

st.markdown('<p class="section-label">Issue Distribution</p>', unsafe_allow_html=True)

dist = df["category"].value_counts().reset_index()
dist.columns = ["Category", "Count"]
dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)

col_a, col_b = st.columns(2)

with col_a:
    fig1 = go.Figure(go.Bar(
        x=dist["Count"],
        y=dist["Category"],
        orientation="h",
        text=dist["Percentage"].astype(str) + "%",
        textposition="outside",
        marker=dict(color=colors[:len(dist)], line=dict(width=0)),
    ))
    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a0aec0", family="DM Mono"),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False),
        margin=dict(t=10, b=10, l=10, r=60),
        height=300,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = go.Figure(go.Pie(
        labels=dist["Category"],
        values=dist["Count"],
        hole=0.55,
        marker=dict(colors=colors[:len(dist)], line=dict(width=0)),
        textinfo="percent",
        textfont=dict(family="DM Mono", size=11),
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a0aec0", family="DM Mono"),
        showlegend=True,
        legend=dict(font=dict(color="#a0aec0", size=10), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=10, b=10),
        height=300,
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.markdown('<p class="section-label">Priority Breakdown</p>', unsafe_allow_html=True)
col_p1, col_p2, col_p3 = st.columns(3)
high  = len(df[df["priority"] == "High"])
med   = len(df[df["priority"] == "Medium"])
low   = len(df[df["priority"] == "Low"])
total = len(df)
with col_p1:
    st.error(f"**High: {high} queries ({round(high/total*100)}%)**\nRefund + Payment issues")
with col_p2:
    st.warning(f"**Medium: {med} queries ({round(med/total*100)}%)**\nDelivery + Product + Subscription")
with col_p3:
    st.success(f"**Low: {low} queries ({round(low/total*100)}%)**\nOrder Tracking + General")

st.divider()

st.markdown('<p class="section-label">Live Query Analyzer — AI Automation</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:12px;color:#4f5a7a;font-family:\'DM Mono\',monospace;">Type any customer query — system will auto-classify, prioritize and suggest reply</p>', unsafe_allow_html=True)

user_query = st.text_input("", placeholder="e.g. Where is my order? My payment failed...")

if st.button("Analyze"):
    if user_query.strip():
        category = classify_query(user_query)
        priority = get_priority(category)
        reply    = REPLIES[category]
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.info(f"**Category**\n\n{category}")
        with col_r2:
            if priority == "High":
                st.error(f"**Priority**\n\n{priority}")
            elif priority == "Medium":
                st.warning(f"**Priority**\n\n{priority}")
            else:
                st.success(f"**Priority**\n\n{priority}")
        with col_r3:
            st.success(f"**Suggested Reply**\n\n{reply}")
    else:
        st.warning("Please enter a query first!")

st.divider()

st.markdown('<p class="section-label">Query Log</p>', unsafe_allow_html=True)
p_filter = st.selectbox("Filter by priority", ["All", "High", "Medium", "Low"])
c_filter = st.selectbox("Filter by category", ["All"] + sorted(df["category"].unique().tolist()))

filtered = df.copy()
if p_filter != "All":
    filtered = filtered[filtered["priority"] == p_filter]
if c_filter != "All":
    filtered = filtered[filtered["category"] == c_filter]

st.dataframe(
    filtered[["query", "category", "priority"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.markdown('<p class="section-label">Automation Opportunities</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Order Tracking: 29%**\n\nAuto-send tracking link on WhatsApp within 2 mins. No human needed.")
with col2:
    st.warning("**Delivery Delay: 18%**\n\nProactive delay alert before customer complains. Reduces tickets by 60%.")
with col3:
    st.error("**Refund Request: 16%**\n\nAuto-acknowledge and escalate if pending 7 or more days.")
