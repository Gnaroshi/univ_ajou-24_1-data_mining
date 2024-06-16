import pandas as pd
import ast

file_path = "../dataset/1000_40.csv"
data = pd.read_csv(file_path)

df = pd.read_csv(file_path)

champions = set()
spells = set()


def extract_champions_and_spells(champion_spell_list):
    for champ, spell1, spell2 in champion_spell_list:
        champions.add(champ)
        spells.add(spell1)
        spells.add(spell2)


for index, row in df.iterrows():
    ourteam_champions_with_spell = ast.literal_eval(row["ourteam_champions_with_spell"])
    enemy_champions_with_spell = ast.literal_eval(row["enemy_champions_with_spell"])

    extract_champions_and_spells(ourteam_champions_with_spell)
    extract_champions_and_spells(enemy_champions_with_spell)

champions = sorted(champions)
spells = sorted(spells)

champion_mapping = {champ: idx + 1 for idx, champ in enumerate(champions)}
spell_mapping = {spell: idx + 1 for idx, spell in enumerate(spells)}


def convert_to_numbers(champion_spell_list):
    return [
        [champion_mapping[champ], spell_mapping[spell1], spell_mapping[spell2]]
        for champ, spell1, spell2 in champion_spell_list
    ]


converted_data = []

for index, row in df.iterrows():
    ourteam_champions_with_spell = ast.literal_eval(row["ourteam_champions_with_spell"])
    enemy_champions_with_spell = ast.literal_eval(row["enemy_champions_with_spell"])
    game_players = ast.literal_eval(row["game_players"])

    converted_ourteam = convert_to_numbers(ourteam_champions_with_spell)
    converted_enemy = convert_to_numbers(enemy_champions_with_spell)

    converted_data.append(
        [
            row["user_ID"],
            row["user_ID_tag"],
            row["result_value"],
            str(converted_ourteam),
            str(converted_enemy),
            str(game_players),
        ]
    )

columns = [
    "user_ID",
    "user_ID_tag",
    "result_value",
    "ourteam_champions_with_spell",
    "enemy_champions_with_spell",
    "game_players",
]
converted_df = pd.DataFrame(converted_data, columns=columns)

converted_df.to_csv("converted_data.csv", index=False)

print("Champion Mapping:")
for champ, idx in champion_mapping.items():
    print(f"{champ}: {idx}")

print("\nSpell Mapping:")
for spell, idx in spell_mapping.items():
    print(f"{spell}: {idx}")

print("Data conversion complete and saved to 'converted_data.csv'")


"""
Champion Mapping:
Aatrox: 1
Ahri: 2
Akali: 3
Akshan: 4
Alistar: 5
Amumu: 6
Anivia: 7
Annie: 8
Aphelios: 9
Ashe: 10
Aurelion Sol: 11
Azir: 12
Bard: 13
Bel'Veth: 14
Blitzcrank: 15
Brand: 16
Braum: 17
Briar: 18
Caitlyn: 19
Camille: 20
Cassiopeia: 21
Cho'Gath: 22
Corki: 23
Darius: 24
Diana: 25
Dr. Mundo: 26
Draven: 27
Ekko: 28
Elise: 29
Evelynn: 30
Ezreal: 31
Fiddlesticks: 32
Fiora: 33
Fizz: 34
Galio: 35
Gangplank: 36
Garen: 37
Gnar: 38
Gragas: 39
Graves: 40
Gwen: 41
Hecarim: 42
Heimerdinger: 43
Hwei: 44
Illaoi: 45
Irelia: 46
Ivern: 47
Janna: 48
Jarvan IV: 49
Jax: 50
Jayce: 51
Jhin: 52
Jinx: 53
K'Sante: 54
Kai'Sa: 55
Kalista: 56
Karma: 57
Karthus: 58
Kassadin: 59
Katarina: 60
Kayle: 61
Kayn: 62
Kennen: 63
Kha'Zix: 64
Kindred: 65
Kled: 66
Kog'Maw: 67
LeBlanc: 68
Lee Sin: 69
Leona: 70
Lillia: 71
Lissandra: 72
Lucian: 73
Lulu: 74
Lux: 75
Malphite: 76
Malzahar: 77
Maokai: 78
Master Yi: 79
Milio: 80
Miss Fortune: 81
Mordekaiser: 82
Morgana: 83
Naafiri: 84
Nami: 85
Nasus: 86
Nautilus: 87
Neeko: 88
Nidalee: 89
Nilah: 90
Nocturne: 91
Nunu & Willump: 92
Olaf: 93
Orianna: 94
Ornn: 95
Pantheon: 96
Poppy: 97
Pyke: 98
Qiyana: 99
Quinn: 100
Rakan: 101
Rammus: 102
Rek'Sai: 103
Rell: 104
Renata Glasc: 105
Renekton: 106
Rengar: 107
Riven: 108
Rumble: 109
Ryze: 110
Samira: 111
Sejuani: 112
Senna: 113
Seraphine: 114
Sett: 115
Shaco: 116
Shen: 117
Shyvana: 118
Singed: 119
Sion: 120
Sivir: 121
Skarner: 122
Smolder: 123
Sona: 124
Soraka: 125
Swain: 126
Sylas: 127
Syndra: 128
Tahm Kench: 129
Taliyah: 130
Talon: 131
Taric: 132
Teemo: 133
Thresh: 134
Tristana: 135
Trundle: 136
Tryndamere: 137
Twisted Fate: 138
Twitch: 139
Udyr: 140
Urgot: 141
Varus: 142
Vayne: 143
Veigar: 144
Vel'Koz: 145
Vex: 146
Vi: 147
Viego: 148
Viktor: 149
Vladimir: 150
Volibear: 151
Warwick: 152
Wukong: 153
Xayah: 154
Xerath: 155
Xin Zhao: 156
Yasuo: 157
Yone: 158
Yorick: 159
Yuumi: 160
Zac: 161
Zed: 162
Zeri: 163
Ziggs: 164
Zilean: 165
Zoe: 166
Zyra: 167

Spell Mapping:
Barrier: 1
Cleanse: 2
Exhaust: 3
Flash: 4
Ghost: 5
Heal: 6
Ignite: 7
Smite: 8
Teleport: 9
"""

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

print("Champion Mapping:", champion_mapping)
print("\nSpell Mapping:", spell_mapping)
