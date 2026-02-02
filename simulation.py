import pandas as pd
import random

HOME_ADV = 0.25
AWAY_PENALTY = 0.05
DRAW_PROB = 0.28

def simulate_match(home, away, strength):
    sh = strength[home] + HOME_ADV
    sa = strength[away] - AWAY_PENALTY

    diff = sh - sa

    if random.random() < DRAW_PROB:
        return 1, 1

    if diff > 0:
        return 3, 0
    else:
        return 0, 3
def simulate_season(table, fixtures):
    points = table["Pts"].to_dict()

    for home, away in fixtures:
        hp, ap = simulate_match(home, away, table["Strength"].to_dict())
        points[home] += hp
        points[away] += ap

    return points
def simulate_season_with_table(table, fixtures):
    points = table["Pts"].to_dict()

    for home, away in fixtures:
        hp, ap = simulate_match(home, away, table["Strength"].to_dict())
        points[home] += hp
        points[away] += ap

    final = (
        pd.Series(points)
        .sort_values(ascending=False)
        .reset_index()
    )
    final.columns = ["Club", "Pts"]

    final["Position"] = range(1, len(final) + 1)

    return final
