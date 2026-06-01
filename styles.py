def load_css():
    
    return """
    <style>

    /* Main Background */

    .stApp {
        background-color: #f5f7fa;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* KPI Cards */

    .metric-card {

        background: linear-gradient(
            135deg,
            #667eea,
            #764ba2
        );

        border-radius: 20px;

        padding: 25px;

        text-align: center;

        color: white;

        box-shadow:
        0px 4px 15px rgba(
            0,
            0,
            0,
            0.15
        );

        margin-bottom: 15px;
    }

    .metric-title {

        font-size: 18px;

        font-weight: bold;

        margin-bottom: 10px;
    }

    .metric-value {

        font-size: 36px;

        font-weight: bold;
    }

    /* Recommendation Cards */

    .recommend-card {

        background-color: white;

        border-radius: 15px;

        padding: 20px;

        margin-bottom: 15px;

        box-shadow:
        0px 2px 10px rgba(
            0,
            0,
            0,
            0.1
        );
    }

    /* Dashboard Titles */

    h1 {

        color: #2c3e50;
    }

    h2 {

        color: #34495e;
    }

    h3 {

        color: #34495e;
    }

    </style>
    """