import pandas as pd

df = pd.read_csv("dataset/PhiUSIIL_Phishing_URL_Dataset.csv")

print(df.columns.tolist())
print("\nDataset Shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())