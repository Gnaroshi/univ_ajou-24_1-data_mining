import pandas as pd
import ast

file_path = "./pp_data.csv"
data = pd.read_csv(file_path)


def extract_champions(team_data):
    champions = []
    for player_data in team_data:
        champions.append(player_data[1])
    return champions


result_values = data["result_value"]
our_teams = data["our_team"].apply(ast.literal_eval)
enemy_teams = data["enemy_team"].apply(ast.literal_eval)

our_team_champions = our_teams.apply(extract_champions)
enemy_team_champions = enemy_teams.apply(extract_champions)

new_data = pd.DataFrame(
    {
        "result_value": result_values,
        "our_team_champions": our_team_champions,
        "enemy_team_champions": enemy_team_champions,
    }
)

new_file_path = "./extracted_data.csv"
new_data.to_csv(new_file_path, index=False)

print(f"New CSV file saved to {new_file_path}")
