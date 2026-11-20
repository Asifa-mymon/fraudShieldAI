
import streamlit as st
import pandas as pd
import joblib
import os

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD FILES ----------------
@st.cache_resource
def load_model():
    return joblib.load("models/fraud_detection_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("data/transactions.csv")

model = load_model()
data = load_data()

# ---------------- DESIGN / CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: radial-gradient(circle at 75% 0%, #102b46 0%, #071526 38%, #030b17 100%);
    color: #e8f3ff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10243d, #071426);
    border-right: 1px solid #164568;
}

[data-testid="stSidebar"] * {
    color: #e5f3ff;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #f3f8ff !important;
}

p, label {
    color: #b9cce0;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #102943, #0a1b30);
    border: 1px solid #17496a;
    border-radius: 15px;
    padding: 18px 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,.22);
}

div[data-testid="stMetric"] label {
    color: #b8cee0 !important;
}

div[data-testid="stMetricValue"] {
    color: #f4faff !important;
}

.stButton button, .stFormSubmitButton button {
    background: linear-gradient(90deg, #00a9bd, #00d6bd);
    color: #031522;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 43px;
}

.stButton button:hover, .stFormSubmitButton button:hover {
    background: #27e3d0;
    color: #031522;
    border: none;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] > div {
    background-color: #10243a;
    color: white;
    border-color: #24516d;
}

[data-testid="stDataFrame"] {
    border: 1px solid #1c4968;
    border-radius: 12px;
}

hr {
    border-color: #1d4561;
}

.brand {
    text-align: center;
    padding: 15px 5px 22px 5px;
    border-bottom: 1px solid #244762;
    margin-bottom: 20px;
}

.brand-icon {
    font-size: 55px;
    color: #00d9ef;
    filter: drop-shadow(0 0 12px #00bcd4);
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    color: #f3f8ff;
}

.brand-tag {
    font-size: 12px;
    color: #9bbbd2;
    letter-spacing: 1px;
}

.hero {
    background: linear-gradient(110deg, #102b47, #07192c 65%, #07334a);
    border: 1px solid #12617c;
    border-radius: 18px;
    padding: 22px 25px;
    margin-bottom: 24px;
    box-shadow: 0 0 25px rgba(0,190,220,.08);
}

.hero-title {
    font-size: 31px;
    font-weight: 800;
    color: white;
}

.hero-sub {
    color: #a9c8dc;
    font-size: 14px;
}

.shield {
    font-size: 65px;
    text-align: center;
    color: #00d9ef;
    text-shadow: 0 0 22px #00cce8;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #edf7ff;
    margin: 12px 0 15px 0;
}

.panel {
    background: linear-gradient(145deg, #102943, #091a2e);
    border: 1px solid #1b4b69;
    border-radius: 15px;
    padding: 19px;
    margin-bottom: 15px;
}

.panel-title {
    font-size: 17px;
    font-weight: 700;
    color: #eaf6ff;
    margin-bottom: 13px;
}

.status {
    background: #073a37;
    border: 1px solid #00a98e;
    border-radius: 10px;
    padding: 12px;
    color: #45f0c3;
    font-weight: 700;
    text-align: center;
}

.small-note {
    color: #91abc1;
    font-size: 12px;
}

.result-card {
    background: linear-gradient(135deg, #102c46, #092033);
    border: 1px solid #087e91;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div class="brand-name">FraudShield AI</div>
        <div class="brand-tag">DETECT • PREVENT • SECURE</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Transaction Analysis", "About Project"],
        label_visibility="visible"
    )

    st.markdown("---")
    st.markdown("### SYSTEM STATUS")
    st.markdown(
        '<div class="status">● &nbsp; ML Model Loaded</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="shield">🔐</div>'
        '<p style="text-align:center;font-size:12px;">'
        'Offline Academic Demonstration</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("**BSIT PROJECT**")
    st.caption("Roll No: 24BSIT-51")

# ---------------- HERO HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="row">
        <div class="hero-title">🛡️ FraudShield <span style="color:#00d9d0;">AI</span></div>
        <div class="hero-sub">Smart Fraud Detection for a Safer Tomorrow</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- DASHBOARD PAGE ----------------
if page == "Dashboard":

    total = len(data)
    fraud = int(data["is_fraud"].sum())
    normal = total - fraud
    fraud_rate = (fraud / total * 100) if total else 0

    st.markdown("## 📊 Security Overview")
    st.caption("Monitor financial transactions and identify suspicious activity.")

    # KPI CARDS
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Transactions", f"{total:,}")
    c2.metric("Fraudulent Records", f"{fraud:,}")
    c3.metric("Normal Records", f"{normal:,}")
    c4.metric("Fraud Rate", f"{fraud_rate:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # CHARTS
    left, right = st.columns([1, 1.5])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">◉ Transaction Distribution</div>',
                    unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;gap:25px;padding:15px 0;">
            <div style="width:155px;height:155px;border-radius:50%;
            background:conic-gradient(#00d4c1 {100-fraud_rate}%,
            #ff5364 0);display:flex;align-items:center;justify-content:center;">
                <div style="width:105px;height:105px;border-radius:50%;
                background:#0b2035;display:flex;flex-direction:column;
                align-items:center;justify-content:center;">
                    <b style="font-size:25px;color:#ffffff;">{fraud_rate:.1f}%</b>
                    <span style="font-size:12px;color:#a9c8dc;">Fraud</span>
                </div>
            </div>
            <div style="font-size:14px;line-height:2.2;color:#dceeff;">
                <span style="color:#00d4c1;">●</span> Normal ({normal:,})<br>
                <span style="color:#ff5364;">●</span> Fraud ({fraud:,})
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">◷ Hourly Transaction Activity</div>',
                    unsafe_allow_html=True)

        hourly = data.groupby("hour").size().reindex(range(24), fill_value=0)
        st.area_chart(hourly, color="#00c9d8", height=230)
        st.markdown('</div>', unsafe_allow_html=True)

    # RECENT RECORDS
    st.markdown('<div class="section-title">▤ Recent Transaction Records</div>',
                unsafe_allow_html=True)

    recent = data.tail(8).copy()
    recent["Status"] = recent["is_fraud"].map({
        0: "Normal",
        1: "Fraud"
    })

    recent = recent.rename(columns={
        "amount": "Amount",
        "hour": "Hour",
        "international": "International",
        "location_mismatch": "Location Mismatch",
        "card_present": "Card Present",
        "transactions_last_24h": "Last 24h"
    })

    recent["Amount"] = recent["Amount"].map(lambda x: f"Rs. {x:,.0f}")
    st.dataframe(
        recent[[
            "Amount", "Hour", "International",
            "Location Mismatch", "Card Present",
            "Last 24h", "Status"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    <div class="status">🛡️ &nbsp; FraudShield AI System Active</div>
    <p class="small-note" style="text-align:center;">
    Academic demonstration using a synthetic transaction dataset.
    </p>
    """, unsafe_allow_html=True)

# ---------------- TRANSACTION ANALYSIS PAGE ----------------
elif page == "Transaction Analysis":

    st.markdown("## 🔍 Transaction Analysis")
    st.caption("Enter transaction details to check its predicted fraud risk.")

    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Transaction Details</div>',
                    unsafe_allow_html=True)

        with st.form("transaction_form"):
            amount = st.number_input(
                "Transaction Amount (Rs.)",
                min_value=100.0,
                max_value=1000000.0,
                value=5000.0,
                step=500.0
            )

            hour = st.slider("Transaction Hour", 0, 23, 14)

            international = st.selectbox(
                "International Transaction",
                ["No", "Yes"]
            )

            location_mismatch = st.selectbox(
                "Location Mismatch",
                ["No", "Yes"]
            )

            card_present = st.selectbox(
                "Card Present",
                ["Yes", "No"]
            )

            transactions_last_24h = st.number_input(
                "Transactions in Last 24 Hours",
                min_value=1,
                max_value=100,
                value=3
            )

            submitted = st.form_submit_button(
                "Analyze Transaction",
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">🛡️ Analysis Information</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        **The ML model checks:**

        - Transaction amount
        - Transaction time
        - International activity
        - Location mismatch
        - Card presence
        - Recent transaction frequency

        <br>
        <div class="status">● Random Forest Model Ready</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        input_data = pd.DataFrame([{
            "amount": amount,
            "hour": hour,
            "international": 1 if international == "Yes" else 0,
            "location_mismatch": 1 if location_mismatch == "Yes" else 0,
            "card_present": 1 if card_present == "Yes" else 0,
            "transactions_last_24h": transactions_last_24h
        }])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        risk_score = probability * 100

        if risk_score < 30:
            risk_level = "LOW RISK"
            risk_color = "#00d4a1"
        elif risk_score < 70:
            risk_level = "MEDIUM RISK"
            risk_color = "#ffbd45"
        else:
            risk_level = "HIGH RISK"
            risk_color = "#ff5364"

        st.markdown("### Analysis Result")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.markdown(f"""
            <div class="result-card">
                <p style="color:#a9c8dc;">PREDICTED STATUS</p>
                <h2 style="color:{risk_color};">
                    {"⚠️ FRAUDULENT" if prediction == 1 else "✓ NORMAL"}
                </h2>
                <p style="color:#d9eafa;">Model Prediction</p>
            </div>
            """, unsafe_allow_html=True)

        with result_col2:
            st.markdown(f"""
            <div class="result-card">
                <p style="color:#a9c8dc;">MODEL FRAUD PROBABILITY</p>
                <h2 style="color:{risk_color};">{risk_score:.1f}%</h2>
                <h4 style="color:{risk_color};">{risk_level}</h4>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### ⚠️ Transaction Risk Indicators")

        reasons = []

        if amount > 35000:
            reasons.append("High transaction amount")
        if international == "Yes":
            reasons.append("International transaction")
        if location_mismatch == "Yes":
            reasons.append("Location mismatch")
        if transactions_last_24h > 10:
            reasons.append("High transaction frequency")
        if 0 < hour < 4:
            reasons.append("Unusual transaction hour")

        if reasons:
            for reason in reasons:
                st.warning(reason)
        else:
            st.success("No major rule-based warning indicators found.")

        st.caption(
            "Note: The risk score is the model's predicted fraud probability. "
            "This is an academic demonstration, not a real banking decision."
        )

# ---------------- ABOUT PROJECT PAGE ----------------
elif page == "About Project":

    st.markdown("## 🛡️ About FraudShield AI")
    st.caption("Intelligent Fraudulent Transaction Detection and Risk Analysis System")

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Project Overview</div>
        FraudShield AI is a machine learning-based academic project that
        analyzes financial transaction patterns and predicts whether a
        transaction may be fraudulent or normal.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Technologies Used")

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Language", "Python")
    t2.metric("ML Algorithm", "Random Forest")
    t3.metric("Data Processing", "Pandas")
    t4.metric("Dashboard", "Streamlit")

    st.markdown("### 🧠 Main Features")

    features = [
        "Machine learning-based fraud prediction",
        "Transaction risk probability",
        "Suspicious pattern indicators",
        "Transaction statistics and charts",
        "Offline local demonstration"
    ]

    for feature in features:
        st.markdown(f"- {feature}")

    st.markdown("### 📌 Project Information")
    st.markdown("""
    - **Project:** FraudShield AI
    - **Student Roll No:** 24BSIT-51
    - **Project Type:** Data Science / Machine Learning
    - **Model:** Random Forest Classifier
    - **Dataset:** Synthetic financial transaction data
    """)

    st.markdown("""
    <div class="status">
        FraudShield AI — Detect • Prevent • Secure
    </div>
    """, unsafe_allow_html=True)
