import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import os
from groq import Groq

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

.stDataFrame { background: rgba(255,255,255,0.02) !important; }

div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8eaf6 !important;
}

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

.auto-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
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

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if not os.path.exists("dataset/classified_queries.csv"):
    subprocess.run(["python", "src/classifier.py"])

df = pd.read_csv("dataset/classified_queries.csv")

# ── HEADER ──────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("## Beastlife Intelligence")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:11px;color:#4f5a7a;">AI CUSTOMER SUPPORT SYSTEM — 2026</p>', unsafe_allow_html=True)
with col_h2:
    st.markdown('<div class="live-badge">● LIVE SYSTEM</div>', unsafe_allow_html=True)

st.divider()

# ── METRICS ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Queries", len(df))
col2.metric("Auto-Resolvable", "71%")
col3.metric("High Priority", len(df[df["priority"] == "High"]))
col4.metric("Categories", df["category"].nunique())

st.divider()

# ── CHARTS ──────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<p class="section-label">Issue Distribution</p>', unsafe_allow_html=True)
    dist = df["category"].value_counts().reset_index()
    dist.columns = ["Category", "Count"]
    dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)

    colors = ["#6366f1","#f59e0b","#ef4444","#ec4899","#06b6d4","#10b981","#8b5cf6"]

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
        height=280,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown('<p class="section-label">Donut Chart</p>', unsafe_allow_html=True)
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
        height=280,
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── PRIORITY ──────────────────────────────────────────
st.markdown('<p class="section-label">Priority Breakdown</p>', unsafe_allow_html=True)
col_p1, col_p2, col_p3 = st.columns(3)
high = len(df[df["priority"] == "High"])
med  = len(df[df["priority"] == "Medium"])
low  = len(df[df["priority"] == "Low"])
total = len(df)
with col_p1:
    st.error(f"**High — {high} queries ({round(high/total*100)}%)**\nRefund + Payment issues")
with col_p2:
    st.warning(f"**Medium — {med} queries ({round(med/total*100)}%)**\nDelivery + Product + Subscription")
with col_p3:
    st.success(f"**Low — {low} queries ({round(low/total*100)}%)**\nOrder Tracking + General")

st.divider()

# ── GROQ AI LIVE ANALYZER ──────────────────────────────────────────
st.markdown('<p class="section-label">Groq AI — Live Query Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:12px;color:#4f5a7a;font-family:\'DM Mono\',monospace;">Type any customer query — Groq AI will classify, prioritize and suggest a reply</p>', unsafe_allow_html=True)

user_query = st.text_input("", placeholder="e.g. Where is my order? / My payment failed...")

if st.button("Analyze with AI"):
    if user_query:
        with st.spinner("Groq AI analyzing..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a customer support AI for Beastlife, a supplement brand.
Analyze the customer query and respond in this exact format:

Category: [one of: Order Tracking, Delivery Delay, Refund Request, Payment Failure, Product Complaint, Subscription Issue, General Question]
Priority: [High / Medium / Low]
Suggested Reply: [a short friendly professional reply to send to the customer]"""
                    },
                    {"role": "user", "content": user_query}
                ]
            )

        result = response.choices[0].message.content
        category, priority, reply = "", "", ""
        for line in result.strip().split("\n"):
            if line.startswith("Category:"):
                category = line.replace("Category:", "").strip()
            elif line.startswith("Priority:"):
                priority = line.replace("Priority:", "").strip()
            elif line.startswith("Suggested Reply:"):
                reply = line.replace("Suggested Reply:", "").strip()

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

st.divider()

# ── QUERY LOG ──────────────────────────────────────────
st.markdown('<p class="section-label">Query Log</p>', unsafe_allow_html=True)
p_filter = st.selectbox("Filter by priority", ["All", "High", "Medium", "Low"])
c_filter = st.selectbox("Filter by category", ["All"] + sorted(df["category"].unique().tolist()))

filtered = df.copy()
if p_filter != "All":
    filtered = filtered[filtered["priority"] == p_filter]
if c_filter != "All":
    filtered = filtered[filtered["category"] == c_filter]

st.dataframe(filtered[["query", "category", "priority"]], use_container_width=True, hide_index=True)

st.divider()

# ── AUTOMATION ──────────────────────────────────────────
st.markdown('<p class="section-label">Automation Opportunities</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Order Tracking — 29%**\n\nAuto-send tracking link on WhatsApp within 2 mins.")
with col2:
    st.warning("**Delivery Delay — 18%**\n\nProactive delay alert before customer complains.")
with col3:
    st.error("**Refund Request — 16%**\n\nAuto-acknowledge + escalate if pending 7+ days.")
```

---

Ye replace karo existing `app.py` se — dark theme, Syne font, Groq AI sab kuch hai! 🔥

Groq key Streamlit secrets mein daal dena:
```
GROQ_API_KEY = "gsk_xxxxxx"
