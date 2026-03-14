import pandas as pd

df = pd.read_csv("dataset/classified_queries.csv")

print("=" * 45)
print("   Beastlife Customer Issue Report")
print("=" * 45)

dist = df["category"].value_counts(normalize=True) * 100

print("\n Issue Distribution:\n")
for cat, pct in dist.items():
    bar = "█" * int(pct / 2)
    print(f"  {cat:<25} {bar} {round(pct, 1)}%")

print("\n Priority Breakdown:\n")
for p in ["High", "Medium", "Low"]:
    count = len(df[df["priority"] == p])
    print(f"  {p:<10} {count} queries")

auto = ["Order Tracking", "Delivery Delay", "General Question"]
auto_count = len(df[df["category"].isin(auto)])
total = len(df)
pct = round((auto_count / total) * 100, 1)

print(f"\n Auto-resolvable: {auto_count}/{total} ({pct}%)")
print(f" Needs human agent: {total - auto_count}/{total} ({round(100 - pct, 1)}%)")
print("\n" + "=" * 45)
