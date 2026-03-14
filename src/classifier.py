import pandas as pd

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

def classify_query(query):
    query = query.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in query:
                return category
    return "General Question"

def get_priority(category):
    high = ["Refund Request", "Payment Failure"]
    medium = ["Delivery Delay", "Product Complaint", "Subscription Issue"]
    if category in high:
        return "High"
    elif category in medium:
        return "Medium"
    return "Low"

df = pd.read_csv("dataset/customer_queries.csv")
df["category"] = df["query"].apply(classify_query)
df["priority"] = df["category"].apply(get_priority)
df.to_csv("dataset/classified_queries.csv", index=False)

print(f"Total queries: {len(df)}")
print(f"Total categories: {df['category'].nunique()}")
print("\n=== Distribution ===")
dist = df["category"].value_counts(normalize=True) * 100
for cat, pct in dist.items():
    print(f"{cat:<25} {round(pct, 1)}%")
