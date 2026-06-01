# 🍽️ Smart Canteen AI Platform

An AI-powered food recommendation and demand prediction system for campus canteens.

The platform combines Machine Learning, Data Analytics, and Interactive Dashboards to provide personalized food recommendations, demand forecasting, wait-time prediction, and business intelligence for canteen management.

---

# 🚀 Features

## 🤖 Personalized Food Recommendation

* Hybrid Recommendation System
* Collaborative Filtering using Cosine Similarity
* User Segmentation using K-Means Clustering
* Personalized food suggestions based on order history and ratings

## 📈 Demand Prediction

* Predicts expected food demand
* Uses Random Forest Regression
* Helps optimize food preparation and inventory planning

## ⏳ Wait Time Prediction

* Predicts food preparation waiting time
* Considers:

  * Food Item
  * Queue Size
  * Available Cooks
  * Preparation Time

## 🤖 AI Food Assistant

* Interactive chatbot interface
* Recommends food based on:

  * User preferences
  * Previous orders
  * Time slot

## 📊 Analytics Dashboard

* Total Orders
* Total Users
* Revenue Analysis
* Top Food Items
* Trending Foods
* Customer Leaderboard
* Interactive Visualizations

## 🛒 Order Management

* Add new food orders
* Live order feed
* Real-time dashboard updates

---

# 🧠 Machine Learning Algorithms

## Recommendation System

* Collaborative Filtering
* Cosine Similarity
* K-Means Clustering

## Demand Forecasting

* Random Forest Regressor

## Wait Time Prediction

* Random Forest Regressor

---

# 🛠️ Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-Learn

### Data Visualization

* Plotly

### Model Persistence

* Pickle

---

# 📁 Project Structure

```text
FOOD_PREDICTION/

├── data/
│   ├── demand_data.csv
│   ├── orders.csv
│   └── wait_time_data.csv
│
├── images/
│   ├── burger.jpg
│   └── idli.jpg
│
├── models/
│   ├── day_encoder.pkl
│   ├── demand_model.pkl
│   ├── food_encoder.pkl
│   ├── kmeans.pkl
│   ├── scaler.pkl
│   └── time_encoder.pkl
│
├── ai_assistant.py
├── analysis.py
├── app.py
├── clustering.py
├── demand_data.py
├── demand_prediction.py
├── food_images.py
├── generate_data.py
├── hybrid_recommendation.py
├── ml_utils.py
├── order_manager.py
├── recommendation.py
├── styles.py
├── users.py
├── wait_time_model.py
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Madhan1822/Food_Recommendation_ML_Project.git

cd Food_Recommendation_ML_Project
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

---

# 📊 Dashboard Modules

## Dashboard

* KPI Cards
* Revenue Tracking
* Live Orders Feed
* Trending Foods
* Top Customers

## Recommendations

* Personalized food suggestions

## Demand Prediction

* Predict future food demand

## Wait Time Prediction

* Estimate preparation waiting time

## AI Assistant

* Food recommendation chatbot

## Place Order

* Simulated real-time ordering

## Analytics

* Interactive charts and reports

---

# 🎯 Project Workflow

```text
User Activity
      ↓
Orders Dataset
      ↓
Data Processing
      ↓
Machine Learning Models
      ↓
Recommendations
Demand Prediction
Wait-Time Prediction
      ↓
Streamlit Dashboard
```

---

# 📈 Business Benefits

* Improves user experience through personalized recommendations
* Reduces food wastage using demand forecasting
* Improves operational efficiency
* Provides decision-making insights through analytics
* Enhances canteen service quality

---

# 🔮 Future Enhancements

* Real-Time Database Integration
* User Authentication System
* Inventory Management Module
* Mobile Application
* Deep Learning Recommendation Engine
* Cloud Deployment
* Voice-Based Food Assistant
* Real-Time Order Tracking

---

# 📄 Resume Description

Developed a Smart Canteen AI Platform using Python, Streamlit, Scikit-Learn, Pandas, and Plotly. Implemented Hybrid Recommendation Systems using Collaborative Filtering and K-Means Clustering, Demand Forecasting using Random Forest Regression, Wait-Time Prediction, AI Chatbot Assistance, Real-Time Order Simulation, and Interactive Analytics Dashboards to improve campus food service intelligence.

---

# 👨‍💻 Author

Madhan E

GitHub:
https://github.com/Madhan1822

Project Repository:
https://github.com/Madhan1822/Food_Recommendation_ML_Project
