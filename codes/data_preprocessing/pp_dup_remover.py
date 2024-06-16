import pandas as pd

df = pd.read_csv("data.csv")
df_unique = df.drop_duplicates()
df_unique.to_csv("unique_file.csv", index=False)
