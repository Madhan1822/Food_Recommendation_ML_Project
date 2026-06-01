import pandas as pd

df = pd.read_csv("data/orders.csv")

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

print(demand_df.head())

demand_df.to_csv(
    "data/demand_data.csv",
    index=False
)

print("\nDemand dataset created successfully!")