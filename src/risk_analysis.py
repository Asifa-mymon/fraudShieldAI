import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Risk Analysis | FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Transaction Risk Analysis")
st.write("Analyze transaction patterns and estimate their model-based risk score.")

# Load model
model = joblib.load("models/fraud_detection_model.pkl")

# Risk thresholds for this demonstration
def get_risk_level(score):
    if score < 30:
        return "Low Risk"
    elif score < 70:
        return "Medium Risk"
    else:
        return "High Risk"

st.subheader("Enter Transaction Details")

with st.form("risk_form"):
    amount = st.number_input("Transaction Amount", min_value=0.0, value=500.0)
    hour = st.slider("Transaction Hour", 0, 23, 12)
    international = st.selectbox("International Transaction", ["No", "Yes"])
    location_mismatch = st.selectbox("Location Mismatch", ["No", "Yes"])
    card_present = st.selectbox("Card Present", ["Yes", "No"])
    transactions_last_24h = st.number_input(
        "Transactions in Last 24 Hours",
        min_value=0,
        value=2
    )

    submitted = st.form_submit_button("Analyze Risk")

if submitted:
    transaction = pd.DataFrame([{
        "amount": amount,
        "hour": hour,
        "international": 1 if international == "Yes" else 0,
        "location_mismatch": 1 if location_mismatch == "Yes" else 0,
        "card_present": 1 if card_present == "Yes" else 0,
        "transactions_last_24h": transactions_last_24h
    }])

    score = model.predict_proba(transaction)[0][1] * 100
    risk = get_risk_level(score)
    prediction = model.predict(transaction)[0]

    st.subheader("Analysis Result")

    st.metric("Model Fraud Score", f"{score:.2f}%")
    st.progress(int(score))

    if risk == "Low Risk":
        st.success("Low Risk")
    elif risk == "Medium Risk":
        st.warning("Medium Risk")
    else:
        st.error("High Risk")

    if prediction == 1:
        st.write("Model Classification: Suspicious / Fraud")
    else:
        st.write("Model Classification: Normal")

    st.info(
        "This is a demonstration score from a model trained on synthetic data. "
        "It is not a calibrated real-world fraud probability or a banking decision."
    )