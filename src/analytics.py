import pandas as pd

df = pd.read_csv("dataset/classified_queries.csv")

issue_distribution = df["category"].value_counts(normalize=True) * 100

print("Customer Issue Distribution (%):")

print(issue_distribution)
