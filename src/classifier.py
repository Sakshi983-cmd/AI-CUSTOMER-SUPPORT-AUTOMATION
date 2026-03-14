import pandas as pd

def classify_query(query):

    query = query.lower()

    if "order" in query or "track" in query:
        return "Order Tracking"

    elif "late" in query or "delay" in query or "transit" in query:
        return "Delivery Delay"

    elif "refund" in query or "return" in query:
        return "Refund Request"

    elif "payment" in query or "charged" in query:
        return "Payment Failure"

    elif "product" in query or "damaged" in query or "broken" in query:
        return "Product Complaint"

    elif "subscription" in query:
        return "Subscription Issue"

    else:
        return "General Question"


df = pd.read_csv("dataset/customer_queries.csv")

df["category"] = df["query"].apply(classify_query)

df.to_csv("dataset/classified_queries.csv", index=False)

print("Classification Completed")
print(df.head())
