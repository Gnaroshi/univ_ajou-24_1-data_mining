from math import comb, factorial

total_champions = 167
bans_per_team = 5
picks_per_team = 5


def combinations(n, k):
    return comb(n, k)


def calculate_possible_games(total_champions, bans_per_team, picks_per_team):
    bans_ways = combinations(total_champions, bans_per_team)
    remaining_champions_after_bans = total_champions - 2 * bans_per_team
    picks_ways = combinations(remaining_champions_after_bans, picks_per_team)
    picks_permutations = picks_ways * factorial(picks_per_team)
    total_possible_games = bans_ways**2 * picks_permutations**2
    return total_possible_games


total_possible_games = calculate_possible_games(
    total_champions, bans_per_team, picks_per_team
)
a = total_possible_games
b = 0
while a > 0:
    if a < 10:
        print(b, a)
        break
    a /= 10
    b += 1

print(f"Total possible games: {total_possible_games}")
