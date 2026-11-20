import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load dataset
data = pd.read_csv("data/transactions.csv")

# Select input features and target
X = data.drop(columns=["transaction_id", "is_fraud"])
y = data["is_fraud"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Load trained model
model = joblib.load("models/fraud_detection_model.pkl")

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
print("\n===== FraudShield AI Model Evaluation =====")

print("\nAccuracy:")
print(f"{accuracy_score(y_test, y_pred) * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Normal", "Fraud"]
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))