import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv("data/transactions.csv")

# Fraud vs Normal Transactions
plt.figure(figsize=(6, 4))
sns.countplot(x="is_fraud", data=data)
plt.title("Fraud vs Normal Transactions")
plt.xlabel("Transaction Type (0 = Normal, 1 = Fraud)")
plt.ylabel("Number of Transactions")
plt.savefig("data/fraud_distribution.png")
plt.show()

# Transaction Amount Distribution
plt.figure(figsize=(6, 4))
sns.histplot(data["amount"], bins=30, kde=True)
plt.title("Transaction Amount Distribution")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")
plt.savefig("data/amount_distribution.png")
plt.show()

# Fraud by Transaction Hour
plt.figure(figsize=(6, 4))
sns.countplot(x="hour", data=data[data["is_fraud"] == 1])
plt.title("Fraud Transactions by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Fraud Transactions")
plt.savefig("data/fraud_by_hour.png")
plt.show()

print("All graphs created successfully!")