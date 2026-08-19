import pandas as pd

df = pd.read_csv("dataset/PhiUSIIL_Phishing_URL_Dataset.csv")

# Keep only numeric columns and label
numeric_df = df.select_dtypes(include=['number'])

numeric_df.to_csv("dataset/processed_dataset.csv", index=False)

print("Processed Dataset Saved!")
print(numeric_df.head())