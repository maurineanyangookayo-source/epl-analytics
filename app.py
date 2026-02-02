import streamlit as st
import pandas as pd

from standings_gw24 import load_standings
from fixtures import load_fixtures
from strength import calculate_strength
from simulation import simulate_season_with_table

st.set_page_config(page_title="EPL Table Predictor", layout="wide")

st.title("📊 EPL Final Table Predictor (GW24 → GW38)")

# Load data
table = load_standings()
fixtures = load_fixtures()

# Calculate strength
table["Strength"] = table.apply(calculate_strength, axis=1)

# Number of simulations
sims = st.slider("Number of simulations", 1000, 20000, 10000, step=1000)

# Run simulations and store full tables
tables = []
for _ in range(sims):
    final_table = simulate_season_with_table(table.copy(), fixtures)
    tables.append(final_table)

# -----------------------------
# Compute average projected points
# -----------------------------

# Build dict of lists to store points for each team
points_dict = {club: [] for club in table.index}

for t in tables:
    for _, row in t.iterrows():
        points_dict[row["Club"]].append(row["Pts"])

# Compute average points per team
avg_points = {club: sum(lst)/len(lst) for club, lst in points_dict.items()}

# Build final projected table
final_table = pd.DataFrame({
    "Club": list(avg_points.keys()),
    "Projected Points": list(avg_points.values())
})
final_table = final_table.sort_values("Projected Points", ascending=False)
final_table["Position"] = range(1, 21)
final_table = final_table.set_index("Position")

# -----------------------------
# Title probabilities
# -----------------------------
title_counts = {}
for t in tables:
    winner = t.iloc[0]["Club"]
    title_counts[winner] = title_counts.get(winner, 0) + 1

title_probs = {team: round((count / sims) * 100, 2) for team, count in title_counts.items()}

# -----------------------------
# Relegation probabilities
# -----------------------------
relegation_counts = {}
for t in tables:
    relegated = t[t["Position"] >= 18]["Club"]
    for team in relegated:
        relegation_counts[team] = relegation_counts.get(team, 0) + 1

relegation_probs = {team: round((count / sims) * 100, 2) for team, count in relegation_counts.items()}

st.subheader("🏆 Title Probability (%)")
st.json(title_probs)

st.subheader("🔻 Relegation Probability (%)")
st.json(relegation_probs)

# -----------------------------
# Finish position distributions
# -----------------------------
position_counts = {}
for t in tables:
    for _, row in t.iterrows():
        club = row["Club"]
        pos = row["Position"]
        position_counts.setdefault(club, {})
        position_counts[club][pos] = position_counts[club].get(pos, 0) + 1

position_probs = {
    club: {pos: round((count / sims) * 100, 2) for pos, count in positions.items()}
    for club, positions in position_counts.items()
}

team = st.selectbox("Select team", sorted(position_probs.keys()))
st.write(position_probs[team])
