def calculate_strength(row):
    ppg = row["Pts"] / row["MP"]
    gdpg = row["GD"] / row["MP"]
    gfpg = row["GF"] / row["MP"]
    form = row["Form"] / 15  # max points = 15 for last 5 matches

    return (0.45 * ppg) + (0.25 * gdpg) + (0.2 * gfpg) + (0.1 * form)
