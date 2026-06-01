import pandas as pd

def add_order(
    user_id,
    food_item,
    price,
    rating,
    time_slot,
    day_of_week
):

    df = pd.read_csv(
        "data/orders.csv"
    )

    new_order = pd.DataFrame(
        [{
            "user_id": user_id,
            "food_item": food_item,
            "price": price,
            "rating": rating,
            "time_slot": time_slot,
            "day_of_week": day_of_week
        }]
    )

    df = pd.concat(
        [df, new_order],
        ignore_index=True
    )

    df.to_csv(
        "data/orders.csv",
        index=False
    )