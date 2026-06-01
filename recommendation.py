import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/orders.csv")

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

def get_similar_users(user_id, top_n=5):

    similar_users = similarity_df[user_id] \
        .sort_values(ascending=False)

    return similar_users[1:top_n+1]

def recommend_food(user_id, top_n=5):

    similar_users = get_similar_users(user_id)

    user_orders = set(
        df[df["user_id"] == user_id]["food_item"]
    )

    recommendations = {}

    for sim_user in similar_users.index:

        foods = df[
            df["user_id"] == sim_user
        ]["food_item"]

        for food in foods:

            if food not in user_orders:

                recommendations[food] = \
                    recommendations.get(food, 0) + 1

    recommendations = sorted(
        recommendations.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

user_id = 101

print("\nPrevious Orders:")
print(
    df[df["user_id"] == user_id]
    ["food_item"]
    .unique()
)

print("\nRecommended Foods:")
print(
    recommend_food(user_id)
)