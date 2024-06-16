import pandas as pd
import ast
import numpy as np

file_path = "./pp_data.csv"
data = pd.read_csv(file_path)


def parse_list_column(column):
    return column.apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


data["our_team_object"] = parse_list_column(data["our_team_object"])
data["enemy_team_object"] = parse_list_column(data["enemy_team_object"])

win_data_our_team = data[data["result_value"] == 1]

win_data_enemy_team_renamed = data[data["result_value"] == 0].rename(
    columns={
        "our_team": "enemy_team",
        "our_team_object": "enemy_team_object",
        "our_team_total_kill": "enemy_team_total_kill",
        "our_team_total_gold": "enemy_team_total_gold",
        "enemy_team": "our_team",
        "enemy_team_object": "our_team_object",
        "enemy_team_total_kill": "our_team_total_kill",
        "enemy_team_total_gold": "our_team_total_gold",
    }
)

win_data = pd.concat([win_data_our_team, win_data_enemy_team_renamed])

game_time_mean = win_data["game_time"].mean()
our_team_total_kill_mean = win_data["our_team_total_kill"].mean()
our_team_total_gold_mean = win_data["our_team_total_gold"].mean()
enemy_team_total_kill_mean = win_data["enemy_team_total_kill"].mean()
enemy_team_total_gold_mean = win_data["enemy_team_total_gold"].mean()


def mean_of_object_column(column):
    object_array = np.array(
        [np.pad(x, (0, 6 - len(x)), "constant", constant_values=0) for x in column]
    )
    return np.mean(object_array, axis=0)


our_team_object_mean = mean_of_object_column(win_data["our_team_object"])
enemy_team_object_mean = mean_of_object_column(win_data["enemy_team_object"])

print("victory:")
print(f"game_time mean: {game_time_mean}")
print(f"our_team_total_kill mean: {our_team_total_kill_mean}")
print(f"our_team_total_gold mean: {our_team_total_gold_mean}")
print(f"enemy_team_total_kill mean: {enemy_team_total_kill_mean}")
print(f"enemy_team_total_gold mean: {enemy_team_total_gold_mean}")

lol_object = ["baron", "dragon", "riftherald", "voidgrub", "tower", "inhibitor"]

for i, obj in enumerate(lol_object):
    print(f"our_team_object {obj} mean: {our_team_object_mean[i]}")
    print(f"enemy_team_object {obj} mean: {enemy_team_object_mean[i]}")
