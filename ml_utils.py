import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/orders.csv")

# =========================
# RECOMMENDATION MODEL
# =========================

user_food_matrix = pd.pivot_table(
    df,
    index="user_id",
    columns="food_item",
    values="rating",
    aggfunc="mean",
    fill_value=0
)

similarity_matrix = cosine_similarity(
    user_food_matrix
)

similarity_df = pd.DataFrame(
    similarity_matrix,
    index=user_food_matrix.index,
    columns=user_food_matrix.index
)

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

# =========================
# RECOMMENDATION FUNCTION
# =========================

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

    similar_users = (
        similarity_df[user_id]
        .sort_values(
            ascending=False
        )[1:6]
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

    time_foods = (
        df[
            df["time_slot"] == time_slot
        ]["food_item"]
        .value_counts()
    )

    for food in time_foods.index:

        scores[food] = (
            scores.get(food, 0) + 2
        )

    for food in (
        df["food_item"]
        .value_counts()
        .index
    ):
        scores[food] = (
            scores.get(food, 0) + 1
        )

    cluster = user_food_matrix.loc[
        user_id,
        "cluster"
    ]

    cluster_foods = (
        cluster_summary
        .loc[cluster]
        .sort_values(
            ascending=False
        )
    )

    for food in cluster_foods.index:

        if food != "cluster":

            scores[food] = (
                scores.get(food, 0) + 2
            )

    for food in user_orders:

        scores.pop(food, None)

    recommendations = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

# =========================
# DEMAND MODEL
# =========================

demand_df = (
    df.groupby(
        [
            "day_of_week",
            "time_slot",
            "food_item"
        ]
    )
    .size()
    .reset_index(name="orders")
)

day_encoder = LabelEncoder()
time_encoder = LabelEncoder()
food_encoder = LabelEncoder()

demand_df["day_encoded"] = day_encoder.fit_transform(
    demand_df["day_of_week"]
)

demand_df["time_encoded"] = time_encoder.fit_transform(
    demand_df["time_slot"]
)

demand_df["food_encoded"] = food_encoder.fit_transform(
    demand_df["food_item"]
)

X = demand_df[
    [
        "day_encoded",
        "time_encoded",
        "food_encoded"
    ]
]

y = demand_df["orders"]

demand_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

demand_model.fit(X, y)

# =========================
# DEMAND FUNCTION
# =========================

def predict_demand(
    day,
    time_slot,
    food_item
):

    day_val = day_encoder.transform(
        [day]
    )[0]

    time_val = time_encoder.transform(
        [time_slot]
    )[0]

    food_val = food_encoder.transform(
        [food_item]
    )[0]

    prediction = demand_model.predict(
        [[
            day_val,
            time_val,
            food_val
        ]]
    )

    return round(prediction[0])