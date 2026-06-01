import pandas as pd
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv("data/demand_data.csv")

print("\n===== DATASET =====")
print(df.head())

# =====================================
# ENCODE CATEGORICAL COLUMNS
# =====================================

day_encoder = LabelEncoder()
time_encoder = LabelEncoder()
food_encoder = LabelEncoder()

df["day_encoded"] = day_encoder.fit_transform(
    df["day_of_week"]
)

df["time_encoded"] = time_encoder.fit_transform(
    df["time_slot"]
)

df["food_encoded"] = food_encoder.fit_transform(
    df["food_item"]
)

# =====================================
# FEATURES & TARGET
# =====================================

X = df[
    [
        "day_encoded",
        "time_encoded",
        "food_encoded"
    ]
]

y = df["orders"]

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# TRAIN MODEL
# =====================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# =====================================
# EVALUATION
# =====================================

predictions = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

print("\n===== MODEL PERFORMANCE =====")
print("Mean Absolute Error :", round(mae, 2))
print("R2 Score            :", round(r2, 2))

# =====================================
# DEMAND PREDICTION FUNCTION
# =====================================

def predict_demand(
    day,
    time_slot,
    food_item
):

    try:

        day_val = day_encoder.transform(
            [day]
        )[0]

        time_val = time_encoder.transform(
            [time_slot]
        )[0]

        food_val = food_encoder.transform(
            [food_item]
        )[0]

        prediction = model.predict(
            [[
                day_val,
                time_val,
                food_val
            ]]
        )

        return round(prediction[0])

    except Exception as e:

        print("Prediction Error:", e)
        return None

# =====================================
# SAMPLE PREDICTIONS
# =====================================

print("\n===== SAMPLE DEMAND PREDICTIONS =====")

foods = sorted(
    df["food_item"].unique()
)

for food in foods:

    predicted_orders = predict_demand(
        "Monday",
        "Lunch",
        food
    )

    print(
        f"{food:<15} -> {predicted_orders} orders"
    )

# =====================================
# SAVE MODEL
# =====================================

pickle.dump(
    model,
    open(
        "models/demand_model.pkl",
        "wb"
    )
)

pickle.dump(
    day_encoder,
    open(
        "models/day_encoder.pkl",
        "wb"
    )
)

pickle.dump(
    time_encoder,
    open(
        "models/time_encoder.pkl",
        "wb"
    )
)

pickle.dump(
    food_encoder,
    open(
        "models/food_encoder.pkl",
        "wb"
    )
)

print("\n===== MODEL SAVED =====")
print("demand_model.pkl")
print("day_encoder.pkl")
print("time_encoder.pkl")
print("food_encoder.pkl")