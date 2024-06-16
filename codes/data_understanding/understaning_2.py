# file_path = "./data_understanding/converted_data.csv"
# data = pd.read_csv(file_path)

import pandas as pd
import matplotlib.pyplot as plt

file_path = "./data_understanding/converted_data.csv"
data = pd.read_csv(file_path)

data["result_value"] = data["result_value"].astype(int)
data["ourteam_champions_with_spell"] = data["ourteam_champions_with_spell"].apply(eval)
data["enemy_champions_with_spell"] = data["enemy_champions_with_spell"].apply(eval)
data["game_players"] = data["game_players"].apply(eval)


def get_champion_combination(champions_with_spells):
    champions = [champ[0] for champ in champions_with_spells]
    return tuple(sorted(champions))


data["ourteam_combination"] = data["ourteam_champions_with_spell"].apply(
    get_champion_combination
)
data["enemy_combination"] = data["enemy_champions_with_spell"].apply(
    get_champion_combination
)

all_combinations = []

for index, row in data.iterrows():
    all_combinations.append([row["ourteam_combination"], 1, 0, 1])
    all_combinations.append([row["enemy_combination"], 0, 1, 1])

combinations_df = pd.DataFrame(
    all_combinations,
    columns=["champion_combination", "win_count", "loss_count", "total_games"],
)

combination_stats = combinations_df.groupby("champion_combination").sum().reset_index()

combination_stats["win_rate"] = (
    combination_stats["win_count"] / combination_stats["total_games"]
)

sorted_combination_stats_by_win_rate = combination_stats.sort_values(
    by="win_rate", ascending=False
)

output_path_win_rate = "champion_combinations_stats_by_win_rate.csv"
sorted_combination_stats_by_win_rate.to_csv(output_path_win_rate, index=False)

sorted_combination_stats_by_total_games = combination_stats.sort_values(
    by="total_games", ascending=False
)

output_path_total_games = "champion_combinations_stats_by_total_games.csv"
sorted_combination_stats_by_total_games.to_csv(output_path_total_games, index=False)

print("Sorted Champion Combinations Stats by Win Rate")
print(sorted_combination_stats_by_win_rate.head(10))

total_games_sum = combination_stats["total_games"].sum()
print(f"Total games sum: {total_games_sum}")

top_combinations_by_win_rate = sorted_combination_stats_by_win_rate.head(10)

plt.figure(figsize=(12, 8))
plt.barh(
    range(len(top_combinations_by_win_rate)),
    top_combinations_by_win_rate["win_rate"],
    align="center",
    color="skyblue",
)
plt.yticks(
    range(len(top_combinations_by_win_rate)),
    [str(combo) for combo in top_combinations_by_win_rate["champion_combination"]],
)
plt.xlabel("Win Rate")
plt.title("Top 10 Champion Combinations by Win Rate")
plt.gca().invert_yaxis()
plt.show()

print(
    sorted_combination_stats_by_win_rate[
        ["champion_combination", "total_games", "win_count", "loss_count", "win_rate"]
    ]
)
