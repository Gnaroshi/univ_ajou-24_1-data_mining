import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score
import ast

file_path = "./pp_data.csv"
data = pd.read_csv(file_path)


def extract_features(row):
    our_team = ast.literal_eval(row["our_team"])
    enemy_team = ast.literal_eval(row["enemy_team"])
    our_team_object = ast.literal_eval(row["our_team_object"])
    enemy_team_object = ast.literal_eval(row["enemy_team_object"])

    our_champions = frozenset([player[1] for player in our_team])
    enemy_champions = frozenset([player[1] for player in enemy_team])

    return our_champions, enemy_champions, our_team_object, enemy_team_object


(
    data["our_team_champs"],
    data["enemy_team_champs"],
    data["our_team_object"],
    data["enemy_team_object"],
) = zip(*data.apply(extract_features, axis=1))

mlb = MultiLabelBinarizer()

X_our = mlb.fit_transform(data["our_team_champs"])
X_enemy = mlb.transform(data["enemy_team_champs"])
X = pd.concat(
    [
        pd.DataFrame(X_our, columns=[f"our_{champ}" for champ in mlb.classes_]),
        pd.DataFrame(X_enemy, columns=[f"enemy_{champ}" for champ in mlb.classes_]),
    ],
    axis=1,
)

X["game_time"] = data["game_time"]
X["our_team_total_kill"] = data["our_team_total_kill"]
X["our_team_total_gold"] = data["our_team_total_gold"]
X["enemy_team_total_kill"] = data["enemy_team_total_kill"]
X["enemy_team_total_gold"] = data["enemy_team_total_gold"]

our_team_object_columns = [
    "our_baron",
    "our_dragon",
    "our_riftherald",
    "our_voidgrub",
    "our_tower",
    "our_inhibitor",
]
enemy_team_object_columns = [
    "enemy_baron",
    "enemy_dragon",
    "enemy_riftherald",
    "enemy_voidgrub",
    "enemy_tower",
    "enemy_inhibitor",
]

X[our_team_object_columns] = pd.DataFrame(
    data["our_team_object"].tolist(), index=data.index
)
X[enemy_team_object_columns] = pd.DataFrame(
    data["enemy_team_object"].tolist(), index=data.index
)

y = data["result_value"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

param_grids = {
    "Random Forest": {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    },
    "Gradient Boosting": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 0.2],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 0.9, 1.0],
    },
    "XGBoost": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 0.2],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 0.9, 1.0],
    },
}

models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "XGBoost": XGBClassifier(
        random_state=42, use_label_encoder=False, eval_metric="logloss"
    ),
}

best_models = {}

for model_name, model in models.items():
    print(f"Starting GridSearchCV for {model_name}...")
    grid_search = GridSearchCV(
        model, param_grids[model_name], cv=5, scoring="accuracy", n_jobs=-1, verbose=2
    )
    grid_search.fit(X_train, y_train)
    best_models[model_name] = grid_search.best_estimator_
    print(f"Best params for {model_name}: {grid_search.best_params_}")
    print(
        f"Best cross-validation accuracy for {model_name}: {grid_search.best_score_:.2f}"
    )

model_results = {}

for model_name, model in best_models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    model_results[model_name] = {"model": model, "accuracy": accuracy}
    print(f"{model_name} Test Accuracy: {accuracy:.2f}")


def predict_best_champions(
    model,
    our_team_partial,
    enemy_team,
    game_time,
    our_team_total_kill,
    our_team_total_gold,
    enemy_team_total_kill,
    enemy_team_total_gold,
    our_team_object,
    enemy_team_object,
    top_n=5,
):
    our_team_set = frozenset(our_team_partial)
    enemy_team_set = frozenset(enemy_team)

    possible_champions = set(mlb.classes_) - our_team_set

    champion_win_rates = []

    for champ in possible_champions:
        our_team_full_set = our_team_set | {champ}

        our_team_encoded = mlb.transform([our_team_full_set])[0]
        enemy_team_encoded = mlb.transform([enemy_team_set])[0]

        input_data = pd.concat(
            [
                pd.DataFrame(
                    [our_team_encoded],
                    columns=[f"our_{champ}" for champ in mlb.classes_],
                ),
                pd.DataFrame(
                    [enemy_team_encoded],
                    columns=[f"enemy_{champ}" for champ in mlb.classes_],
                ),
            ],
            axis=1,
        )

        input_data["game_time"] = game_time
        input_data["our_team_total_kill"] = our_team_total_kill
        input_data["our_team_total_gold"] = our_team_total_gold
        input_data["enemy_team_total_kill"] = enemy_team_total_kill
        input_data["enemy_team_total_gold"] = enemy_team_total_gold

        input_data[our_team_object_columns] = pd.DataFrame(
            [our_team_object], columns=our_team_object_columns
        )
        input_data[enemy_team_object_columns] = pd.DataFrame(
            [enemy_team_object], columns=enemy_team_object_columns
        )

        win_prob = model.predict_proba(input_data)[:, 1][0]

        champion_win_rates.append((champ, win_prob))

    champion_win_rates.sort(key=lambda x: x[1], reverse=True)

    return champion_win_rates[:top_n]


our_team_partial = ["Skarner", "Graves", "Twisted Fate", "Rakan"]
enemy_team = ["Jayce", "Fiddlesticks", "Kayle", "Corki", "Braum"]
game_time = 1449
our_team_total_kill = 30
our_team_total_gold = 53270
enemy_team_total_kill = 18
enemy_team_total_gold = 44910
our_team_object = [1, 2, 1, 3, 7, 1]
enemy_team_object = [0, 1, 0, 2, 2, 0]

for model_name, result in model_results.items():
    top_champions = predict_best_champions(
        result["model"],
        our_team_partial,
        enemy_team,
        game_time,
        our_team_total_kill,
        our_team_total_gold,
        enemy_team_total_kill,
        enemy_team_total_gold,
        our_team_object,
        enemy_team_object,
        top_n=5,
    )
    print(f"\nTop 5 recommended champions by {model_name}:")
    for champ, win_rate in top_champions:
        print(f"{champ}: {win_rate:.2%}")
