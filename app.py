import streamlit as st
import pandas as pd
import plotly.express as px

from ml_utils import (
    hybrid_recommendation,
    predict_demand
)

from wait_time_model import (
    predict_wait_time
)

from ai_assistant import (
    get_ai_response
)

from order_manager import (
    add_order
)

from styles import load_css

# =====================================
# FOOD EMOJIS
# =====================================

FOOD_EMOJIS = {
    "Burger": "🍔",
    "Pizza": "🍕",
    "Dosa": "🥞",
    "Idli": "⚪",
    "Meals": "🍛",
    "Tea": "☕",
    "Coffee": "☕",
    "Sandwich": "🥪",
    "Fried Rice": "🍚",
    "Noodles": "🍜"
}

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Smart Canteen AI",
    page_icon="🍽",
    layout="wide"
)

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# =====================================
# LOAD DATA
# =====================================

@st.cache_data(ttl=5)
def load_data():

    return pd.read_csv(
        "data/orders.csv"
    )

df = load_data()

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🍽 Smart Canteen AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Recommendations",
        "Demand Prediction",
        "Wait Time Prediction",
        "AI Assistant",
        "Place Order",
        "Analytics"
    ]
)

# =====================================
# DASHBOARD
# =====================================

if page == "Dashboard":

    st.title(
        "🍽 Smart Campus Food Intelligence Platform"
    )

    st.write(
        "AI-Powered Recommendation & Demand Prediction System"
    )

    total_orders = len(df)

    total_users = (
        df["user_id"]
        .nunique()
    )

    total_revenue = (
        df["price"]
        .sum()
    )

    popular_food = (
        df["food_item"]
        .value_counts()
        .idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">
            Orders
            </div>
            <div class="metric-value">
            {total_orders}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">
            Users
            </div>
            <div class="metric-value">
            {total_users}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">
            Revenue
            </div>
            <div class="metric-value">
            ₹{total_revenue}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">
            Top Food
            </div>
            <div class="metric-value">
            {popular_food}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.metric(
        "Total Orders",
        len(
            pd.read_csv(
                "data/orders.csv"
            )
        )
    )

    st.subheader(
        "📦 Live Orders Feed"
    )

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )

    st.subheader(
        "🏆 Trending Foods"
    )

    trending = (
        df["food_item"]
        .value_counts()
        .head(5)
    )

    for i, (food, count) in enumerate(
        trending.items(),
        start=1
    ):

        st.write(
            f"{i}. {food} ({count} orders)"
        )

    st.subheader(
        "👤 Top Customers"
    )

    top_users = (
        df["user_id"]
        .value_counts()
        .head(5)
    )

    for user, orders in top_users.items():

        st.write(
            f"User {user}: {orders} orders"
        )
        
# =====================================
# RECOMMENDATIONS
# =====================================

elif page == "Recommendations":

    st.title(
        "🤖 Personalized Food Recommendations"
    )

    user_id = st.selectbox(
        "Select User",
        sorted(
            df["user_id"].unique()
        )
    )

    time_slot = st.selectbox(
        "Time Slot",
        [
            "Morning",
            "Lunch",
            "Evening"
        ]
    )

    if st.button(
        "Get Recommendations"
    ):

        previous_orders = (
            df[df["user_id"] == user_id]
            ["food_item"]
            .unique()
        )

        st.subheader(
            "🛒 Previous Orders"
        )

        cols = st.columns(
            min(
                len(previous_orders),
                5
            )
        )

        for i, food in enumerate(
            previous_orders
        ):

            cols[
                i % len(cols)
            ].info(food)

        recommendations = (
            hybrid_recommendation(
                user_id,
                time_slot
            )
        )

        st.divider()

        st.subheader(
            "⭐ Recommended Foods"
        )

        if len(recommendations) == 0:

            st.warning(
                "No recommendations available"
            )

        else:

            for rank, (
                food,
                score
            ) in enumerate(
                recommendations,
                start=1
            ):

                emoji = FOOD_EMOJIS.get(
                    food,
                    "🍽"
                )

                st.markdown(
                    f"""
                    <div class="metric-card">

                    <h2>
                    #{rank} {emoji} {food}
                    </h2>

                    <h3>
                    Recommendation Score:
                    {score}
                    </h3>

                    </div>

                    <br>
                    """,
                    unsafe_allow_html=True
                )
# =====================================
# DEMAND PREDICTION
# =====================================

elif page == "Demand Prediction":

    st.title(
        "📈 Demand Prediction"
    )

    day = st.selectbox(
        "Select Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    )

    time_slot = st.selectbox(
        "Select Time Slot",
        [
            "Morning",
            "Lunch",
            "Evening"
        ]
    )

    food_item = st.selectbox(
        "Select Food",
        sorted(
            df["food_item"]
            .unique()
        )
    )

    if st.button(
        "Predict Demand"
    ):

        prediction = predict_demand(
            day,
            time_slot,
            food_item
        )

        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-title">
            📈 Expected Orders
            </div>

            <div class="metric-value">
            {prediction}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            f"Prepare approximately {prediction} servings."
        )

# =====================================
# ANALYTICS
# =====================================

elif page == "Analytics":

    st.title(
        "📊 Analytics Dashboard"
    )

    food_df = (
        df["food_item"]
        .value_counts()
        .reset_index()
    )

    food_df.columns = [
        "Food",
        "Orders"
    ]

    fig_food = px.bar(
        food_df,
        x="Food",
        y="Orders",
        title="Popular Food Items"
    )

    revenue_df = (
        df.groupby(
            "food_item"
        )["price"]
        .sum()
        .reset_index()
    )

    fig_revenue = px.pie(
        revenue_df,
        values="price",
        names="food_item",
        title="Revenue Distribution"
    )

    time_df = (
        df.groupby(
            "time_slot"
        )
        .size()
        .reset_index(
            name="Orders"
        )
    )

    fig_time = px.bar(
        time_df,
        x="time_slot",
        y="Orders",
        title="Orders By Time Slot"
    )

    rating_df = (
        df.groupby(
            "food_item"
        )["rating"]
        .mean()
        .reset_index()
    )

    fig_rating = px.bar(
        rating_df,
        x="food_item",
        y="rating",
        title="Average Ratings"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            fig_food,
            use_container_width=True
        )

    with col2:

        st.plotly_chart(
            fig_revenue,
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    with col3:

        st.plotly_chart(
            fig_time,
            use_container_width=True
        )

    with col4:

        st.plotly_chart(
            fig_rating,
            use_container_width=True
        )

    st.divider()

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="canteen_report.csv",
        mime="text/csv"
    )

elif page == "Wait Time Prediction":
    
    st.title(
        "⏳ Smart Queue Prediction"
    )

    food_item = st.selectbox(
        "Food Item",
        [
            "Burger",
            "Pizza",
            "Dosa",
            "Coffee",
            "Sandwich"
        ]
    )

    queue_size = st.slider(
        "Orders In Queue",
        1,
        50,
        10
    )

    cooks = st.slider(
        "Available Cooks",
        1,
        10,
        2
    )

    prep_time = st.slider(
        "Preparation Time",
        1,
        20,
        5
    )

    if st.button(
        "Predict Wait Time"
    ):

        prediction = (
            predict_wait_time(
                food_item,
                queue_size,
                cooks,
                prep_time
            )
        )

        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-title">
            Estimated Wait Time
            </div>

            <div class="metric-value">
            {prediction} mins
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if prediction <= 5:

            st.success(
                "Fast Service 🚀"
            )

        elif prediction <= 10:

            st.warning(
                "Moderate Wait ⏳"
            )

        else:

            st.error(
                "Long Queue ⚠️"
            )
elif page == "AI Assistant":
    
    st.title(
        "🤖 Food AI Assistant"
    )

    user_id = st.selectbox(
        "Select User",
        sorted(
            df["user_id"].unique()
        )
    )

    question = st.text_input(
        "Ask something..."
    )

    if st.button(
        "Ask AI"
    ):

        answer = (
            get_ai_response(
                user_id,
                question
            )
        )

        st.success(
            answer
        )

elif page == "Place Order":
    
    st.title(
        "🛒 Place New Order"
    )

    user_id = st.selectbox(
        "User",
        sorted(
            df["user_id"]
            .unique()
        )
    )

    food_item = st.selectbox(
        "Food Item",
        sorted(
            df["food_item"]
            .unique()
        )
    )

    price = st.number_input(
        "Price",
        min_value=1
    )

    rating = st.slider(
        "Rating",
        1,
        5,
        4
    )

    time_slot = st.selectbox(
        "Time Slot",
        [
            "Morning",
            "Lunch",
            "Evening"
        ]
    )

    day_of_week = st.selectbox(
        "Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    )

    if st.button(
        "Place Order"
    ):

        add_order(
            user_id,
            food_item,
            price,
            rating,
            time_slot,
            day_of_week
        )

        st.success(
            "Order Placed Successfully!"
        )

        st.balloons()