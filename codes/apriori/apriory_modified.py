import pandas as pd
from itertools import combinations
from collections import defaultdict
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt

file_path = "./extracted_data.csv"
data = pd.read_csv(file_path)

adc_data_path = "./OP_GG_Data_adc.csv"
adc_data = pd.read_csv(adc_data_path)

adc_data["플레이 수"] = pd.to_numeric(adc_data["플레이 수"], errors="coerce")
adc_data["승률"] = adc_data["승률"].str.rstrip("%").astype("float") / 100.0

print(adc_data.head())

adc_data = adc_data[["챔피언", "플레이 수", "승률"]]

min_play_count = 50
filtered_adc_data = adc_data[adc_data["플레이 수"] >= min_play_count]

print(filtered_adc_data.head())

data["our_team_champions"] = data["our_team_champions"].apply(eval)
data["enemy_team_champions"] = data["enemy_team_champions"].apply(eval)

win_champions = data[data["result_value"] == 1]["our_team_champions"]
lose_champions = data[data["result_value"] == 0]["enemy_team_champions"]


def get_champion_combinations(team_data):
    combinations_list = []
    for champions in team_data:
        combinations_list.extend(combinations(champions, 2))
    return combinations_list


win_combinations = get_champion_combinations(win_champions)
loss_combinations = get_champion_combinations(lose_champions)

combination_counts = defaultdict(lambda: [0, 0])

for comb in win_combinations:
    combination_counts[comb][0] += 1

for comb in loss_combinations:
    combination_counts[comb][1] += 1

results = []
for comb, counts in combination_counts.items():
    win_count = counts[0]
    loss_count = counts[1]
    total_count = win_count + loss_count
    win_rate = win_count / total_count if total_count > 0 else 0
    results.append([comb[0], comb[1], win_count, loss_count, total_count, win_rate])

results_df = pd.DataFrame(
    results,
    columns=[
        "Champion1",
        "Champion2",
        "WinCount",
        "LossCount",
        "TotalCount",
        "WinRate",
    ],
)

plt.hist(results_df["TotalCount"], bins=50, edgecolor="k")
plt.xlabel("TotalCount")
plt.ylabel("Frequency")
plt.title("Distribution of TotalCount")
plt.show()

total_count_freq = results_df["TotalCount"].value_counts().sort_index()

print("TotalCount 값의 빈도:")
for count, freq in total_count_freq.items():
    print(f"TotalCount가 {count}인 조합의 수는 {freq}입니다.")

threshold = results_df["TotalCount"].median()

print(f"설정된 TotalCount 임계값: {threshold}")

filtered_results_df = results_df[results_df["TotalCount"] >= threshold].copy()
filtered_results_df.sort_values(by="WinRate", ascending=False, inplace=True)

top_5_combinations = filtered_results_df
print("상위 5개의 승률이 높은 챔피언 조합:")
print(top_5_combinations.head(5))

filtered_results_df.to_csv("./champion_combinations_by_winrate.csv", index=False)

sorted_by_total_count_df = filtered_results_df.sort_values(
    by="TotalCount", ascending=False
)
sorted_by_total_count_df.to_csv(
    "./champion_combinations_by_totalcount.csv", index=False
)

print(
    "CSV 파일로 저장되었습니다: champion_combinations_by_winrate.csv, champion_combinations_by_totalcount.csv"
)

top_10_total_count = results_df.sort_values(by="TotalCount", ascending=False).head(10)
print("TotalCount가 가장 많은 순서대로 상위 10개 조합:")
print(top_10_total_count)

transactions = win_champions.tolist()

itemset = set(champion for sublist in transactions for champion in sublist)
encoded_vals = []
for instance in transactions:
    encoded_instance = {item: (1 if item in instance else 0) for item in itemset}
    encoded_vals.append(encoded_instance)

encoded_df = pd.DataFrame(encoded_vals)

encoded_df = encoded_df.astype(bool)

frequent_itemsets = apriori(encoded_df, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)


def recommend_champions_with_weighted_factors(
    selected_champion, rules, results_df, adc_data, top_n=5
):
    recommendations = rules[
        rules["antecedents"].apply(lambda x: selected_champion in list(x))
    ]
    if not recommendations.empty:
        recommendations = recommendations.copy()

        recommendations["total_count"] = recommendations["consequents"].apply(
            lambda x: results_df[
                (results_df["Champion1"].isin(x)) | (results_df["Champion2"].isin(x))
            ]["TotalCount"].sum()
        )
        recommendations["adc_win_rate"] = recommendations["consequents"].apply(
            lambda x: (
                adc_data[adc_data["챔피언"].isin(x)]["승률"].mean()
                if not adc_data[adc_data["챔피언"].isin(x)].empty
                else 0
            )
        )
        recommendations["combo_win_rate"] = recommendations["consequents"].apply(
            lambda x: results_df[
                (results_df["Champion1"].isin(x)) | (results_df["Champion2"].isin(x))
            ]["WinRate"].mean()
        )

        w_confidence = 0.5
        w_total_count = 0.3
        w_adc_win_rate = 0.1
        w_combo_win_rate = 0.1

        recommendations["weighted_score"] = (
            w_confidence * recommendations["confidence"]
            + w_total_count * recommendations["total_count"]
            + w_adc_win_rate * recommendations["adc_win_rate"]
            + w_combo_win_rate * recommendations["combo_win_rate"]
        )

        recommendations = recommendations.sort_values(
            by="weighted_score", ascending=False
        )

        recommended_champions = []
        for consequents in recommendations["consequents"]:
            recommended_champions.extend(list(consequents))

        recommended_champions = list(set(recommended_champions))
        return recommended_champions[:top_n]
    else:
        return ["No recommendations available"]


recommended_champions_all = []
for index, row in top_5_combinations.iterrows():
    selected_champion = row["Champion1"]
    recommended_champions = recommend_champions_with_weighted_factors(
        selected_champion, rules, results_df, filtered_adc_data
    )
    recommended_champions_all.append([selected_champion, recommended_champions])

recommended_df = pd.DataFrame(
    recommended_champions_all, columns=["Champion", "RecommendedChampions"]
)

recommended_df.to_csv("./recommended_champions.csv", index=False)

print("추천 챔피언 CSV 파일로 저장되었습니다: recommended_champions.csv")

selected_champion = "Lucian"
recommended_champions_lucian = recommend_champions_with_weighted_factors(
    selected_champion, rules, results_df, filtered_adc_data
)
print(
    f"챔피언 {selected_champion}을 선택한 경우 추천 챔피언: {recommended_champions_lucian}"
)
selected_champion = "Kai'Sa"
recommended_champions_lucian = recommend_champions_with_weighted_factors(
    selected_champion, rules, results_df, filtered_adc_data
)
print(
    f"챔피언 {selected_champion}을 선택한 경우 추천 챔피언: {recommended_champions_lucian}"
)
selected_champion = "Ashe"
recommended_champions_lucian = recommend_champions_with_weighted_factors(
    selected_champion, rules, results_df, filtered_adc_data
)
print(
    f"챔피언 {selected_champion}을 선택한 경우 추천 챔피언: {recommended_champions_lucian}"
)
