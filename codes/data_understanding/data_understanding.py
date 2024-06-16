import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import itertools

file_path = "./pp_data.csv"
data = pd.read_csv(file_path)

win_loss_data = data["result_value"].value_counts().reset_index()
win_loss_data.columns = ["Result", "Count"]
win_loss_data["Result"] = win_loss_data["Result"].map({1: "Win", 0: "Loss"})

win_loss_data.to_csv("win_loss_analysis.csv", index=False)

plt.figure(figsize=(6, 6))
plt.pie(
    win_loss_data["Count"],
    labels=win_loss_data["Result"],
    autopct="%1.1f%%",
    startangle=140,
)
plt.title("Win/Loss Analysis")
plt.savefig("win_loss_analysis.png")
plt.show()

all_champions = []
all_spells = []

for team in data["our_team"]:
    players = eval(team)
    for player in players:
        all_champions.append(player[1])
        all_spells.extend([player[2], player[3]])

champion_counts = Counter(all_champions).most_common(10)
spell_counts = Counter(all_spells).most_common(10)

champion_df = pd.DataFrame(champion_counts, columns=["Champion", "Count"])
spell_df = pd.DataFrame(spell_counts, columns=["Spell", "Count"])

champion_df.to_csv("champion_play_count.csv", index=False)
spell_df.to_csv("spell_usage_count.csv", index=False)

plt.figure(figsize=(10, 6))
plt.bar(champion_df["Champion"], champion_df["Count"], color="skyblue")
plt.title("Top 10 Champions by Play Count")
plt.xlabel("Champion")
plt.ylabel("Play Count")
plt.xticks(rotation=45)
plt.savefig("champion_play_count.png")
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(spell_df["Spell"], spell_df["Count"], color="lightcoral")
plt.title("Top 10 Spells by Usage Count")
plt.xlabel("Spell")
plt.ylabel("Usage Count")
plt.xticks(rotation=45)
plt.savefig("spell_usage_count.png")
plt.show()

champion_wins = Counter()
champion_games = Counter()

for index, row in data.iterrows():
    result = row["result_value"]
    players = eval(row["our_team"])
    for player in players:
        champion_games[player[1]] += 1
        if result == 1:
            champion_wins[player[1]] += 1

champion_winrate = {
    champion: (champion_wins[champion] / count, count)
    for champion, count in champion_games.items()
}

champion_winrate_df = pd.DataFrame.from_dict(
    champion_winrate, orient="index", columns=["Win Rate", "Games Played"]
).reset_index()
champion_winrate_df.columns = ["Champion", "Win Rate", "Games Played"]
champion_winrate_df = champion_winrate_df.sort_values(
    by="Win Rate", ascending=False
).head(10)

champion_winrate_df.to_csv("champion_winrate.csv", index=False)

plt.figure(figsize=(10, 6))
plt.bar(
    champion_winrate_df["Champion"], champion_winrate_df["Win Rate"], color="limegreen"
)
plt.title("Top 10 Champions by Win Rate")
plt.xlabel("Champion")
plt.ylabel("Win Rate")
plt.xticks(rotation=45)
plt.savefig("champion_winrate.png")
plt.show()

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

combination_winrate = [
    (
        comb,
        combination_wins[comb],
        combination_games[comb] - combination_wins[comb],
        combination_games[comb],
        combination_wins[comb] / combination_games[comb],
    )
    for comb in combination_games
]
combination_winrate_df = pd.DataFrame(
    combination_winrate,
    columns=["Combination", "Wins", "Losses", "Total Games", "Win Rate"],
)
combination_winrate_df = combination_winrate_df.sort_values(
    by="Win Rate", ascending=False
)

combination_winrate_df.to_csv("all_combination_winrate.csv", index=False)

top_combinations = combination_winrate_df.head(10)
plt.figure(figsize=(12, 8))
plt.barh(
    top_combinations["Combination"].astype(str),
    top_combinations["Win Rate"],
    color="gold",
)
plt.title("Top 10 Champion Combinations by Win Rate")
plt.xlabel("Win Rate")
plt.ylabel("Champion Combination")
plt.savefig("top_combination_winrate.png")
plt.show()

top_combinations.to_csv("top_combinations_winrate.csv", index=False)

worst_combinations = combination_winrate_df.tail(10)
plt.figure(figsize=(12, 8))
plt.barh(
    worst_combinations["Combination"].astype(str),
    worst_combinations["Win Rate"],
    color="tomato",
)
plt.title("Bottom 10 Champion Combinations by Win Rate")
plt.xlabel("Win Rate")
plt.ylabel("Champion Combination")
plt.savefig("worst_combination_winrate.png")
plt.show()

worst_combinations.to_csv("worst_combination_winrate.csv", index=False)
