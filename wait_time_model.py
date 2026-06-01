import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# =========================
# LOAD DATA
# =========================

df = pd.read_csv(
    "data/wait_time_data.csv"
)

# =========================
# ENCODE FOOD
# =========================

food_encoder = LabelEncoder()

df["food_encoded"] = (
    food_encoder.fit_transform(
        df["food_item"]
    )
)

# =========================
# FEATURES
# =========================

X = df[
    [
        "food_encoded",
        "orders_in_queue",
        "cooks_available",
        "prep_time"
    ]
]

y = df["wait_time"]

# =========================
# MODEL
# =========================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# =========================
# FUNCTION
# =========================

def predict_wait_time(
    food_item,
    queue_size,
    cooks,
    prep_time
):

    food = (
        food_encoder.transform(
            [food_item]
        )[0]
    )

    prediction = model.predict(
        [[
            food,
            queue_size,
            cooks,
            prep_time
        ]]
    )

    return round(
        prediction[0]
    )