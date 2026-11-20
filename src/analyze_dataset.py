import pandas as pd

# Load dataset
data = pd.read_csv("data/transactions.csv")

print("FRAUDSHIELD AI - DATA ANALYSIS")

print("\nDataset Shape:")
print(data.shape)

print("\nColumn Information:")
print(data.info())

print("\nMissing Values:")
print(data.isnull().sum())

print("\nTransaction Statistics:")
print(data.describe())

print("\nFraud Distribution:")
print(data["is_fraud"].value_counts())

print("\nFraud Percentage:")
print(data["is_fraud"].value_counts(normalize=True) * 100)

print("\nAnalysis Completed Successfully!")