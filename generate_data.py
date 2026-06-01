import pandas as pd
import random
import os

food_items = [
    "Dosa",
    "Idli",
    "Meals",
    "Burger",
    "Pizza",
    "Coffee",
    "Tea",
    "Fried Rice",
    "Noodles",
    "Sandwich"
]

time_slots = [
    "Morning",
    "Lunch",
    "Evening"
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

prices = {
    "Dosa": 40,
    "Idli": 30,
    "Meals": 100,
    "Burger": 80,
    "Pizza": 120,
    "Coffee": 20,
    "Tea": 15,
    "Fried Rice": 120,
    "Noodles": 90,
    "Sandwich": 50
}

os.makedirs("data", exist_ok=True)

data = []

for order_id in range(1, 501):

    user_id = random.randint(101, 150)

    food = random.choice(food_items)

    time_slot = random.choice(time_slots)

    day = random.choice(days)

    rating = random.randint(3, 5)

    data.append([
        order_id,
        user_id,
        food,
        time_slot,
        day,
        prices[food],
        rating
    ])

df = pd.DataFrame(
    data,
    columns=[
        "order_id",
        "user_id",
        "food_item",
        "time_slot",
        "day_of_week",
        "price",
        "rating"
    ]
)

df.to_csv("data/orders.csv", index=False)

print("Dataset Created Successfully")
print(df.head())