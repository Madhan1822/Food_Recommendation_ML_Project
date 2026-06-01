import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/orders.csv")

print("\n===== FIRST 5 RECORDS =====")
print(df.head())

print("\n===== DATA INFO =====")
print(df.info())

print("\n===== STATISTICS =====")
print(df.describe())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== FOOD POPULARITY =====")
print(df["food_item"].value_counts())

print("\n===== ORDERS BY TIME SLOT =====")
print(df.groupby("time_slot").size())

print("\n===== AVERAGE RATINGS =====")
print(
    df.groupby("food_item")["rating"]
    .mean()
    .sort_values(ascending=False)
)

total_revenue = df["price"].sum()

print("\n===== TOTAL REVENUE =====")
print(total_revenue)

print("\n===== REVENUE BY FOOD =====")

food_revenue = (
    df.groupby("food_item")["price"]
    .sum()
    .sort_values(ascending=False)
)

print(food_revenue)

# Popular food chart

plt.figure(figsize=(8, 5))

df["food_item"].value_counts().plot(kind="bar")

plt.title("Popular Food Items")
plt.xlabel("Food")
plt.ylabel("Orders")

plt.tight_layout()

plt.show()