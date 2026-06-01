import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ----------------------------
# LOAD DATA
# ----------------------------

df = pd.read_csv("data/orders.csv")

# ----------------------------
# USER-FOOD MATRIX
# ----------------------------

user_food_matrix = pd.pivot_table(
    df,
    index="user_id",
    columns="food_item",
    values="rating",
    aggfunc="mean",
    fill_value=0
)

# ----------------------------
# USER SIMILARITY
# ----------------------------

similarity_matrix = cosine_similarity(
    user_food_matrix
)

similarity_df = pd.DataFrame(
    similarity_matrix,
    index=user_food_matrix.index,
    columns=user_food_matrix.index
)

# ----------------------------
# CLUSTERING
# ----------------------------

scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    user_food_matrix
)

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(
    scaled_data
)

user_food_matrix["cluster"] = clusters

cluster_summary = (
    user_food_matrix
    .groupby("cluster")
    .mean()
)

# ----------------------------
# SIMILAR USERS
# ----------------------------

def get_similar_users(user_id, top_n=5):

    if user_id not in similarity_df.index:
        return pd.Series()

    similar_users = (
        similarity_df[user_id]
        .sort_values(ascending=False)
    )

    return similar_users[1:top_n+1]

# ----------------------------
# TIME-BASED POPULAR FOODS
# ----------------------------

def get_time_based_foods(time_slot):

    foods = (
        df[df["time_slot"] == time_slot]
        ["food_item"]
        .value_counts()
    )

    return foods

# ----------------------------
# OVERALL POPULAR FOODS
# ----------------------------

def get_popular_foods():

    return (
        df["food_item"]
        .value_counts()
    )

# ----------------------------
# USER CLUSTER
# ----------------------------

def get_user_cluster(user_id):

    if user_id not in user_food_matrix.index:
        return None

    return user_food_matrix.loc[
        user_id,
        "cluster"
    ]

# ----------------------------
# CLUSTER FOODS
# ----------------------------

def cluster_foods(user_id):

    cluster = get_user_cluster(
        user_id
    )

    if cluster is None:
        return pd.Series()

    foods = cluster_summary.loc[
        cluster
    ]

    foods = foods.sort_values(
        ascending=False
    )

    return foods

# ----------------------------
# USER HISTORY
# ----------------------------

def user_history(user_id):

    foods = (
        df[df["user_id"] == user_id]
        ["food_item"]
        .unique()
    )

    return foods

# ----------------------------
# HYBRID RECOMMENDATION
# ----------------------------

def hybrid_recommendation(
    user_id,
    time_slot,
    top_n=5
):

    scores = {}

    user_orders = set(
        df[df["user_id"] == user_id]
        ["food_item"]
    )

    # Similar users contribution
    similar_users = get_similar_users(
        user_id
    )

    for sim_user in similar_users.index:

        foods = df[
            df["user_id"] == sim_user
        ]["food_item"]

        for food in foods:

            if food not in user_orders:

                scores[food] = (
                    scores.get(food, 0) + 3
                )

    # Time-based contribution
    time_foods = get_time_based_foods(
        time_slot
    )

    for food in time_foods.index:

        scores[food] = (
            scores.get(food, 0) + 2
        )

    # Popular foods contribution
    popular_foods = get_popular_foods()

    for food in popular_foods.index:

        scores[food] = (
            scores.get(food, 0) + 1
        )

    # Cluster contribution
    cluster_rec = cluster_foods(
        user_id
    )

    for food in cluster_rec.index:

        if food != "cluster":

            scores[food] = (
                scores.get(food, 0) + 2
            )

    # Remove already ordered foods
    for food in user_orders:

        scores.pop(food, None)

    recommendations = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

# ----------------------------
# TEST
# ----------------------------

user_id = 101
time_slot = "Morning"

print("=" * 50)
print("USER ID:", user_id)
print("=" * 50)

print("\nPREVIOUS ORDERS:")

history = user_history(user_id)

for item in history:
    print("-", item)

print("\nTOP RECOMMENDATIONS:")

recommendations = hybrid_recommendation(
    user_id,
    time_slot,
    top_n=5
)

for food, score in recommendations:
    print(f"{food}  | Score: {score}")