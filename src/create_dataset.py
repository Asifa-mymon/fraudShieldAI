import pandas as pd
import numpy as np

# Generate 5000 transactions
np.random.seed(42)
n = 5000

data = pd.DataFrame({
    "transaction_id": range(1, n + 1),
    "amount": np.random.uniform(100, 50000, n),
    "hour": np.random.randint(0, 24, n),
    "international": np.random.randint(0, 2, n),
    "location_mismatch": np.random.randint(0, 2, n),
    "card_present": np.random.randint(0, 2, n),
    "transactions_last_24h": np.random.randint(1, 15, n)
})


# Calculate demonstration risk points
risk = (
    (data["amount"] > 35000).astype(int)
    + data["international"]
    + data["location_mismatch"]
    + (data["transactions_last_24h"] > 10).astype(int)
    + ((data["hour"] > 0) & (data["hour"] < 4)).astype(int)
)

# Create demonstration fraud labels
data["is_fraud"] = (
    (risk >= 3) & (np.random.random(n) > 0.25)
).astype(int)

# Save dataset
data.to_csv("data/transactions.csv", index=False)

print("Dataset created successfully!")
print("Total Transactions:", len(data))
print("Fraud Transactions:", data["is_fraud"].sum())
print("Normal Transactions:", (data["is_fraud"] == 0).sum())

print("\nDataset Preview:")
print(data.head())