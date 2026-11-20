import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/fraud_detection_model.pkl")

print("================================")
print("       FRAUDSHIELD AI")
print("   Transaction Risk Analysis")
print("================================")

# Get transaction details
amount = float(input("Enter transaction amount: "))
hour = int(input("Enter transaction hour (0-23): "))
international = int(input("International transaction? (1=Yes, 0=No): "))
location_mismatch = int(input("Location mismatch? (1=Yes, 0=No): "))
card_present = int(input("Card present? (1=Yes, 0=No): "))
transactions_last_24h = int(input("Transactions in last 24 hours: "))

# Prepare input data
new_transaction = pd.DataFrame([{
    "amount": amount,
    "hour": hour,
    "international": international,
    "location_mismatch": location_mismatch,
    "card_present": card_present,
    "transactions_last_24h": transactions_last_24h
}])

# Predict transaction
prediction = model.predict(new_transaction)[0]
probability = model.predict_proba(new_transaction)[0][1]

# Display result
print("\n========== ANALYSIS RESULT ==========")

if prediction == 1:
    print("Status: SUSPICIOUS TRANSACTION")
else:
    print("Status: NORMAL TRANSACTION")

print(f"Model Risk Score: {probability * 100:.2f}%")
print("=====================================")