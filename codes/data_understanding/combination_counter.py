import pandas as pd
from collections import Counter

file_path = "./pp_data.csv"
data = pd.read_csv(file_path)

combination_wins = Counter()
combination_games = Counter()

for index, row in data.iterrows():
    result = row["result_value"]
    players = eval(row["our_team"])
    champions = sorted([player[1] for player in players])
    combination = tuple(champions)
    combination_games[combination] += 1
    if result == 1:
        combination_wins[combination] += 1

combination_data = [
    (
        comb,
        combination_wins[comb],
        combination_games[comb] - combination_wins[comb],
        combination_games[comb],
    )
    for comb in combination_games
]

combination_df = pd.DataFrame(
    combination_data, columns=["Combination", "Wins", "Losses", "Total Games"]
)
combination_df = combination_df.sort_values(by="Total Games", ascending=False)

combination_df.to_csv("combination_games_sorted.csv", index=False)

print("CSV 파일이 성공적으로 저장되었습니다: combination_games_sorted.csv")
