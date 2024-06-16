champion_mapping = {
    "Aatrox": 1,
    "Ahri": 2,
    "Akali": 3,
    "Akshan": 4,
    "Alistar": 5,
    "Amumu": 6,
    "Anivia": 7,
    "Annie": 8,
    "Aphelios": 9,
    "Ashe": 10,
    "Aurelion Sol": 11,
    "Azir": 12,
    "Bard": 13,
    "Bel'Veth": 14,
    "Blitzcrank": 15,
    "Brand": 16,
    "Braum": 17,
    "Briar": 18,
    "Caitlyn": 19,
    "Camille": 20,
    "Cassiopeia": 21,
    "Cho'Gath": 22,
    "Corki": 23,
    "Darius": 24,
    "Diana": 25,
    "Dr. Mundo": 26,
    "Draven": 27,
    "Ekko": 28,
    "Elise": 29,
    "Evelynn": 30,
    "Ezreal": 31,
    "Fiddlesticks": 32,
    "Fiora": 33,
    "Fizz": 34,
    "Galio": 35,
    "Gangplank": 36,
    "Garen": 37,
    "Gnar": 38,
    "Gragas": 39,
    "Graves": 40,
    "Gwen": 41,
    "Hecarim": 42,
    "Heimerdinger": 43,
    "Hwei": 44,
    "Illaoi": 45,
    "Irelia": 46,
    "Ivern": 47,
    "Janna": 48,
    "Jarvan IV": 49,
    "Jax": 50,
    "Jayce": 51,
    "Jhin": 52,
    "Jinx": 53,
    "K'Sante": 54,
    "Kai'Sa": 55,
    "Kalista": 56,
    "Karma": 57,
    "Karthus": 58,
    "Kassadin": 59,
    "Katarina": 60,
    "Kayle": 61,
    "Kayn": 62,
    "Kennen": 63,
    "Kha'Zix": 64,
    "Kindred": 65,
    "Kled": 66,
    "Kog'Maw": 67,
    "LeBlanc": 68,
    "Lee Sin": 69,
    "Leona": 70,
    "Lillia": 71,
    "Lissandra": 72,
    "Lucian": 73,
    "Lulu": 74,
    "Lux": 75,
    "Malphite": 76,
    "Malzahar": 77,
    "Maokai": 78,
    "Master Yi": 79,
    "Milio": 80,
    "Miss Fortune": 81,
    "Mordekaiser": 82,
    "Morgana": 83,
    "Naafiri": 84,
    "Nami": 85,
    "Nasus": 86,
    "Nautilus": 87,
    "Neeko": 88,
    "Nidalee": 89,
    "Nilah": 90,
    "Nocturne": 91,
    "Nunu & Willump": 92,
    "Olaf": 93,
    "Orianna": 94,
    "Ornn": 95,
    "Pantheon": 96,
    "Poppy": 97,
    "Pyke": 98,
    "Qiyana": 99,
    "Quinn": 100,
    "Rakan": 101,
    "Rammus": 102,
    "Rek'Sai": 103,
    "Rell": 104,
    "Renata Glasc": 105,
    "Renekton": 106,
    "Rengar": 107,
    "Riven": 108,
    "Rumble": 109,
    "Ryze": 110,
    "Samira": 111,
    "Sejuani": 112,
    "Senna": 113,
    "Seraphine": 114,
    "Sett": 115,
    "Shaco": 116,
    "Shen": 117,
    "Shyvana": 118,
    "Singed": 119,
    "Sion": 120,
    "Sivir": 121,
    "Skarner": 122,
    "Smolder": 123,
    "Sona": 124,
    "Soraka": 125,
    "Swain": 126,
    "Sylas": 127,
    "Syndra": 128,
    "Tahm Kench": 129,
    "Taliyah": 130,
    "Talon": 131,
    "Taric": 132,
    "Teemo": 133,
    "Thresh": 134,
    "Tristana": 135,
    "Trundle": 136,
    "Tryndamere": 137,
    "Twisted Fate": 138,
    "Twitch": 139,
    "Udyr": 140,
    "Urgot": 141,
    "Varus": 142,
    "Vayne": 143,
    "Veigar": 144,
    "Vel'Koz": 145,
    "Vex": 146,
    "Vi": 147,
    "Viego": 148,
    "Viktor": 149,
    "Vladimir": 150,
    "Volibear": 151,
    "Warwick": 152,
    "Wukong": 153,
    "Xayah": 154,
    "Xerath": 155,
    "Xin Zhao": 156,
    "Yasuo": 157,
    "Yone": 158,
    "Yorick": 159,
    "Yuumi": 160,
    "Zac": 161,
    "Zed": 162,
    "Zeri": 163,
    "Ziggs": 164,
    "Zilean": 165,
    "Zoe": 166,
    "Zyra": 167,
}

spell_mapping = {
    "Barrier": 1,
    "Cleanse": 2,
    "Exhaust": 3,
    "Flash": 4,
    "Ghost": 5,
    "Heal": 6,
    "Ignite": 7,
    "Smite": 8,
    "Teleport": 9,
}

# file_path = "./data_understanding/converted_data.csv"
# data = pd.read_csv(file_path)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from collections import Counter
from itertools import combinations
from tqdm import tqdm

file_path = "./data_understanding/converted_data.csv"
data = pd.read_csv(file_path)

data["ourteam_champions_with_spell"] = data["ourteam_champions_with_spell"].apply(
    ast.literal_eval
)
data["enemy_champions_with_spell"] = data["enemy_champions_with_spell"].apply(
    ast.literal_eval
)
data["game_players"] = data["game_players"].apply(ast.literal_eval)


def tuple_champion_names(champion_data):
    return tuple(sorted([entry[0] for entry in champion_data]))


our_combinations = data["ourteam_champions_with_spell"].map(tuple_champion_names)
enemy_combinations = data["enemy_champions_with_spell"].map(tuple_champion_names)

all_combinations = pd.concat([our_combinations, enemy_combinations])
combination_count = Counter(all_combinations)


def calculate_win_rate(combinations, data):
    combination_win_rate = {}
    for combination in tqdm(
        combinations, desc="Calculating win rates for combinations"
    ):
        games_with_combination = data[our_combinations == combination]
        total_games = len(games_with_combination)
        wins = games_with_combination[games_with_combination["result_value"] > 0].shape[
            0
        ]
        win_rate = wins / total_games if total_games > 0 else 0
        combination_win_rate[combination] = win_rate
    return combination_win_rate


combination_win_rate = calculate_win_rate(combination_count, data)

top_win_rate_combinations = pd.DataFrame(
    sorted(combination_win_rate.items(), key=lambda item: item[1], reverse=True)[:10],
    columns=["Combination", "Win Rate"],
)
bottom_win_rate_combinations = pd.DataFrame(
    sorted(combination_win_rate.items(), key=lambda item: item[1])[:10],
    columns=["Combination", "Win Rate"],
)

pair_combinations = []
pair_win_rates = []

for idx, row in tqdm(
    data.iterrows(), desc="Processing pair combinations", total=len(data)
):
    if row["result_value"] > 0:
        champions = [entry[0] for entry in row["ourteam_champions_with_spell"]]
        for pair in combinations(champions, 2):
            pair_combinations.append(tuple(sorted(pair)))

pair_combination_count = Counter(pair_combinations)

pair_combination_win_rate = {}
for pair, count in tqdm(
    pair_combination_count.items(), desc="Calculating win rates for pair combinations"
):
    games_with_pair = sum(
        1 for comb in our_combinations if pair[0] in comb and pair[1] in comb
    )
    wins_with_pair = sum(
        1
        for idx, row in data.iterrows()
        if row["result_value"] > 0
        and pair[0] in [entry[0] for entry in row["ourteam_champions_with_spell"]]
        and pair[1] in [entry[0] for entry in row["ourteam_champions_with_spell"]]
    )
    win_rate = wins_with_pair / games_with_pair if games_with_pair > 0 else 0
    pair_combination_win_rate[pair] = win_rate

top_pair_win_rate_combinations = pd.DataFrame(
    sorted(pair_combination_win_rate.items(), key=lambda item: item[1], reverse=True)[
        :10
    ],
    columns=["Combination", "Win Rate"],
)
bottom_pair_win_rate_combinations = pd.DataFrame(
    sorted(pair_combination_win_rate.items(), key=lambda item: item[1])[:10],
    columns=["Combination", "Win Rate"],
)

plt.figure(figsize=(12, 8))
sns.barplot(data=top_win_rate_combinations, x="Win Rate", y="Combination")
plt.title("Top 10 Champion Combinations by Win Rate")
plt.show()

plt.figure(figsize=(12, 8))
sns.barplot(data=bottom_win_rate_combinations, x="Win Rate", y="Combination")
plt.title("Bottom 10 Champion Combinations by Win Rate")
plt.show()

plt.figure(figsize=(12, 8))
sns.barplot(data=top_pair_win_rate_combinations, x="Win Rate", y="Combination")
plt.title("Top 10 Two-Champion Combinations by Win Rate")
plt.show()

plt.figure(figsize=(12, 8))
sns.barplot(data=bottom_pair_win_rate_combinations, x="Win Rate", y="Combination")
plt.title("Bottom 10 Two-Champion Combinations by Win Rate")
plt.show()
