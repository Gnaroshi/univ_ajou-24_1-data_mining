# file_path = "./data_understanding/converted_data.csv"
# data = pd.read_csv(file_path)

import pandas as pd
import matplotlib.pyplot as plt


champion_mapping = {
    1: "Aatrox",
    2: "Ahri",
    3: "Akali",
    4: "Akshan",
    5: "Alistar",
    6: "Amumu",
    7: "Anivia",
    8: "Annie",
    9: "Aphelios",
    10: "Ashe",
    11: "Aurelion Sol",
    12: "Azir",
    13: "Bard",
    14: "Bel'Veth",
    15: "Blitzcrank",
    16: "Brand",
    17: "Braum",
    18: "Briar",
    19: "Caitlyn",
    20: "Camille",
    21: "Cassiopeia",
    22: "Cho'Gath",
    23: "Corki",
    24: "Darius",
    25: "Diana",
    26: "Dr. Mundo",
    27: "Draven",
    28: "Ekko",
    29: "Elise",
    30: "Evelynn",
    31: "Ezreal",
    32: "Fiddlesticks",
    33: "Fiora",
    34: "Fizz",
    35: "Galio",
    36: "Gangplank",
    37: "Garen",
    38: "Gnar",
    39: "Gragas",
    40: "Graves",
    41: "Gwen",
    42: "Hecarim",
    43: "Heimerdinger",
    44: "Hwei",
    45: "Illaoi",
    46: "Irelia",
    47: "Ivern",
    48: "Janna",
    49: "Jarvan IV",
    50: "Jax",
    51: "Jayce",
    52: "Jhin",
    53: "Jinx",
    54: "K'Sante",
    55: "Kai'Sa",
    56: "Kalista",
    57: "Karma",
    58: "Karthus",
    59: "Kassadin",
    60: "Katarina",
    61: "Kayle",
    62: "Kayn",
    63: "Kennen",
    64: "Kha'Zix",
    65: "Kindred",
    66: "Kled",
    67: "Kog'Maw",
    68: "LeBlanc",
    69: "Lee Sin",
    70: "Leona",
    71: "Lillia",
    72: "Lissandra",
    73: "Lucian",
    74: "Lulu",
    75: "Lux",
    76: "Malphite",
    77: "Malzahar",
    78: "Maokai",
    79: "Master Yi",
    80: "Milio",
    81: "Miss Fortune",
    82: "Mordekaiser",
    83: "Morgana",
    84: "Naafiri",
    85: "Nami",
    86: "Nasus",
    87: "Nautilus",
    88: "Neeko",
    89: "Nidalee",
    90: "Nilah",
    91: "Nocturne",
    92: "Nunu & Willump",
    93: "Olaf",
    94: "Orianna",
    95: "Ornn",
    96: "Pantheon",
    97: "Poppy",
    98: "Pyke",
    99: "Qiyana",
    100: "Quinn",
    101: "Rakan",
    102: "Rammus",
    103: "Rek'Sai",
    104: "Rell",
    105: "Renata Glasc",
    106: "Renekton",
    107: "Rengar",
    108: "Riven",
    109: "Rumble",
    110: "Ryze",
    111: "Samira",
    112: "Sejuani",
    113: "Senna",
    114: "Seraphine",
    115: "Sett",
    116: "Shaco",
    117: "Shen",
    118: "Shyvana",
    119: "Singed",
    120: "Sion",
    121: "Sivir",
    122: "Skarner",
    123: "Smolder",
    124: "Sona",
    125: "Soraka",
    126: "Swain",
    127: "Sylas",
    128: "Syndra",
    129: "Tahm Kench",
    130: "Taliyah",
    131: "Talon",
    132: "Taric",
    133: "Teemo",
    134: "Thresh",
    135: "Tristana",
    136: "Trundle",
    137: "Tryndamere",
    138: "Twisted Fate",
    139: "Twitch",
    140: "Udyr",
    141: "Urgot",
    142: "Varus",
    143: "Vayne",
    144: "Veigar",
    145: "Vel'Koz",
    146: "Vex",
    147: "Vi",
    148: "Viego",
    149: "Viktor",
    150: "Vladimir",
    151: "Volibear",
    152: "Warwick",
    153: "Wukong",
    154: "Xayah",
    155: "Xerath",
    156: "Xin Zhao",
    157: "Yasuo",
    158: "Yone",
    159: "Yorick",
    160: "Yuumi",
    161: "Zac",
    162: "Zed",
    163: "Zeri",
    164: "Ziggs",
    165: "Zilean",
    166: "Zoe",
    167: "Zyra",
}


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


sorted_combination_stats_by_total_games = combination_stats.sort_values(
    by="total_games", ascending=False
)


output_path_win_rate = "champion_combinations_stats_by_win_rate.csv"
sorted_combination_stats_by_win_rate.to_csv(output_path_win_rate, index=False)


output_path_total_games = "champion_combinations_stats_by_total_games.csv"
sorted_combination_stats_by_total_games.to_csv(output_path_total_games, index=False)


def convert_combination_to_names(combination, mapping):
    return tuple(mapping[champ_id] for champ_id in combination)


sorted_combination_stats_by_win_rate["champion_combination"] = (
    sorted_combination_stats_by_win_rate["champion_combination"].apply(
        lambda x: convert_combination_to_names(x, champion_mapping)
    )
)
sorted_combination_stats_by_total_games["champion_combination"] = (
    sorted_combination_stats_by_total_games["champion_combination"].apply(
        lambda x: convert_combination_to_names(x, champion_mapping)
    )
)


output_path_win_rate_names = "champion_combinations_stats_by_win_rate_with_names.csv"
sorted_combination_stats_by_win_rate.to_csv(output_path_win_rate_names, index=False)

output_path_total_games_names = (
    "champion_combinations_stats_by_total_games_with_names.csv"
)
sorted_combination_stats_by_total_games.to_csv(
    output_path_total_games_names, index=False
)


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
