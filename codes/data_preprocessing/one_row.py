import pandas as pd

# 데이터 로드
file_path = "./unique_data.csv"
data = pd.read_csv(file_path)


def print_game_details(game_row):
    game_details = {
        "Row Number": game_row.name,
        "User ID": game_row["user_ID"],
        "User ID Tag": game_row["user_ID_tag"],
        "Result Value": game_row["result_value"],
        "Game Time": game_row["game_time"],
        "Our Team": eval(game_row["our_team"]),
        "Our Team Object": eval(game_row["our_team_object"]),
        "Our Team Total Kill": game_row["our_team_total_kill"],
        "Our Team Total Gold": game_row["our_team_total_gold"],
        "Enemy Team": eval(game_row["enemy_team"]),
        "Enemy Team Object": eval(game_row["enemy_team_object"]),
        "Enemy Team Total Kill": game_row["enemy_team_total_kill"],
        "Enemy Team Total Gold": game_row["enemy_team_total_gold"],
        "Game Players": game_row["game_players"],
    }

    print(f"Row Number: {game_details['Row Number']}")
    print(f"User ID: {game_details['User ID']}")
    print(f"User ID Tag: {game_details['User ID Tag']}")
    print(f"Result Value: {game_details['Result Value']}")
    print(f"Game Time: {game_details['Game Time']} seconds")
    print("\nOur Team:")
    for player in game_details["Our Team"]:
        print(
            f"  - Lane: {player[0]}, Champion: {player[1]}, Spells: {player[2]}, {player[3]}, Kill: {player[4]}, Death: {player[5]}, Assist: {player[6]}, Total Damage: {player[7]}, Total Taken Damage: {player[8]}, Wards: {player[9]}, CS: {player[10]}"
        )
    print(
        f"Our Team Object: Baron: {game_details['Our Team Object'][0]}, Dragon: {game_details['Our Team Object'][1]}, Rift Herald: {game_details['Our Team Object'][2]}, Voidgrub: {game_details['Our Team Object'][3]}, Tower: {game_details['Our Team Object'][4]}, Inhibitor: {game_details['Our Team Object'][5]}"
    )
    print(f"Our Team Total Kill: {game_details['Our Team Total Kill']}")
    print(f"Our Team Total Gold: {game_details['Our Team Total Gold']}")

    print("\nEnemy Team:")
    for player in game_details["Enemy Team"]:
        print(
            f"  - Lane: {player[0]}, Champion: {player[1]}, Spells: {player[2]}, {player[3]}, Kill: {player[4]}, Death: {player[5]}, Assist: {player[6]}, Total Damage: {player[7]}, Total Taken Damage: {player[8]}, Wards: {player[9]}, CS: {player[10]}"
        )
    print(
        f"Enemy Team Object: Baron: {game_details['Enemy Team Object'][0]}, Dragon: {game_details['Enemy Team Object'][1]}, Rift Herald: {game_details['Enemy Team Object'][2]}, Voidgrub: {game_details['Enemy Team Object'][3]}, Tower: {game_details['Enemy Team Object'][4]}, Inhibitor: {game_details['Enemy Team Object'][5]}"
    )
    print(f"Enemy Team Total Kill: {game_details['Enemy Team Total Kill']}")
    print(f"Enemy Team Total Gold: {game_details['Enemy Team Total Gold']}")

    print(f"Game Players: {game_details['Game Players']}")


if __name__ == "__main__":
    print_game_details(data.iloc[0])
