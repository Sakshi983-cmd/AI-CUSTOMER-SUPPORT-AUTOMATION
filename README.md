# 🤖 Beastlife — AI Customer Support Intelligence

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square)
![Plotly](https://img.shields.io/badge/Plotly-Charts-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> Automatically classify customer queries · Visualize issue trends · Identify automation opportunities

---

## 🔄 How It Works
```
📱 Customer Query (WhatsApp / Instagram / Email)
            │
            ▼
    ┌───────────────────┐
    │   AI Classifier   │  ← src/classifier.py
    │  7 Smart Categories│
    └────────┬──────────┘
             │
             ▼
    ┌───────────────────┐
    │    Analytics      │  ← src/analytics.py
    │  Priority Scoring │
    └────────┬──────────┘
             │
             ▼
    ┌───────────────────┐
    │    Dashboard      │  ← dashboard/app.py
    │  Streamlit+Plotly │
    └───────────────────┘
```

---

## 📊 Issue Distribution
```
Order Tracking     ████████████████████████████░  29%  🟢 Low
Delivery Delay     ████████████████████░░░░░░░░░  18%  🟡 Medium  
Refund Request     ████████████████░░░░░░░░░░░░░  16%  🔴 High
Payment Failure    █████████████░░░░░░░░░░░░░░░░  13%  🔴 High
Product Complaint  ███████████░░░░░░░░░░░░░░░░░░  11%  🟡 Medium
Subscription Issue █████████░░░░░░░░░░░░░░░░░░░░   9%  🟡 Medium
General Question   ████░░░░░░░░░░░░░░░░░░░░░░░░░   4%  🟢 Low
```

---

## ⚡ Automation Opportunities

| Issue | Volume | Automation | Impact |
|---|---|---|---|
| Order Tracking | 29% | Auto-send tracking link on WhatsApp | 🔴 High |
| Delivery Delay | 18% | Proactive delay alert before complaint | 🔴 High |
| Refund Request | 16% | Auto-acknowledge + initiate workflow | 🟡 Medium |
| Payment Failure | 13% | Auto-detect duplicate + retry link | 🟡 Medium |
| Subscription | 9% | Chatbot handles pause/upgrade/renewal | 🟢 Low |

> **71% of queries can be auto-resolved** — only 29% need human agent

---

## 🛠️ Tech Stack
```
Classification  →  Python (keyword scoring)
Dashboard       →  Streamlit + Plotly  
Data Layer      →  Pandas
Automation      →  n8n / Make (suggested)
Channels        →  WhatsApp API + Instagram API (suggested)
Scale-up        →  Claude API / OpenAI API (plug-in ready)
```

---

## 🚀 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run classifier
python src/classifier.py

# Launch dashboard
streamlit run dashboard/app.py
```

---

## 📁 Project Structure
```
beastlife-support-ai/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .env.example
├── 📂 dataset/
│   ├── customer_queries.csv
│   └── classified_queries.csv
├── 📂 src/
│   ├── classifier.py
│   └── analytics.py
└── 📂 dashboard/
    └── app.py
```

---

## 📈 Scalability Plan

| Volume | Solution |
|---|---|
| 100 queries/day | Current system — works perfectly |
| 1,000 queries/day | Add caching + batch processing |
| 10,000 queries/day | Plug in Claude API / OpenAI API |
| 100,000 queries/day | Vector database + LangChain pipeline |

---

<div align="center">
Built for Beastlife AI Customer Support Challenge
</div>
