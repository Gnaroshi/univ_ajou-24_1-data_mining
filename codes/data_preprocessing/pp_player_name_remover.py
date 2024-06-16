import pandas as pd

df = pd.read_csv("unique_data.csv")
df = df.drop(columns=["user_ID"])
df = df.drop(columns=["user_ID_tag"])
df = df.drop(columns=["game_players"])
df.to_csv("data_without_game_players.csv", index=False)
