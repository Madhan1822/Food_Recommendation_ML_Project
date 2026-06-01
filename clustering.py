import pandas as pd
import pickle
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

df = pd.read_csv("data/orders.csv")

print("\n===== DATA LOADED =====")
print(df.head())

# USER-FOOD MATRIX

user_food_matrix = pd.pivot_table(
    df,
    index="user_id",
    columns="food_item",
    values="rating",
    aggfunc="mean",
    fill_value=0
)

print("\n===== USER FOOD MATRIX =====")
print(user_food_matrix.head())

# SCALING

scaler = StandardScaler()

scaled_data = scaler.fit_transform(user_food_matrix)

# K-MEANS

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(scaled_data)

user_food_matrix["cluster"] = clusters

print("\n===== CLUSTER ASSIGNMENT =====")
print(user_food_matrix.head())

print("\n===== CLUSTER DISTRIBUTION =====")
print(
    user_food_matrix["cluster"]
    .value_counts()
)

# CLUSTER SUMMARY

print("\n===== CLUSTER SUMMARY =====")

cluster_summary = (
    user_food_matrix
    .groupby("cluster")
    .mean()
)

print(cluster_summary)

# PCA VISUALIZATION

pca = PCA(n_components=2)

reduced = pca.fit_transform(scaled_data)

plt.figure(figsize=(8, 5))

plt.scatter(
    reduced[:, 0],
    reduced[:, 1],
    c=clusters
)

plt.title("Student Clusters")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")

plt.show()

# SAVE MODEL

os.makedirs("models", exist_ok=True)

pickle.dump(
    kmeans,
    open("models/kmeans.pkl", "wb")
)

pickle.dump(
    scaler,
    open("models/scaler.pkl", "wb")
)

print("\nModel Saved Successfully")