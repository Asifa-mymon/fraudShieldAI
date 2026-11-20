import streamlit as st
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

st.set_page_config(
    page_title="Model Performance | FraudShield AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Model Performance")
st.write("Evaluate how well FraudShield AI detects suspicious transactions.")

# Load dataset and model
data = pd.read_csv("data/transactions.csv")
model = joblib.load("models/fraud_detection_model.pkl")

# Prepare testing data
X = data.drop(columns=["transaction_id", "is_fraud"])
y = data["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Predictions
y_pred = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred) * 100
precision = precision_score(y_test, y_pred) * 100
recall = recall_score(y_test, y_pred) * 100
f1 = f1_score(y_test, y_pred) * 100

# Display metrics
st.subheader("Evaluation Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", f"{accuracy:.2f}%")
col2.metric("Precision", f"{precision:.2f}%")
col3.metric("Recall", f"{recall:.2f}%")
col4.metric("F1-Score", f"{f1:.2f}%")

# Confusion Matrix
st.subheader("Confusion Matrix")

cm = confusion_matrix(y_test, y_pred)

cm_df = pd.DataFrame(
    cm,
    index=["Actual Normal", "Actual Fraud"],
    columns=["Predicted Normal", "Predicted Fraud"]
)

st.dataframe(cm_df, use_container_width=True)

# Explanation
st.subheader("Understanding the Results")

st.write(f"- Correct normal transactions: {cm[0][0]}")
st.write(f"- Normal transactions flagged as fraud: {cm[0][1]}")
st.write(f"- Fraud transactions missed: {cm[1][0]}")
st.write(f"- Correctly detected fraud transactions: {cm[1][1]}")

st.info(
    "Note: These results are based on a synthetic demonstration dataset. "
    "They do not represent real-world banking performance."
)