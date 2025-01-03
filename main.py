import asyncio
from typing import List
from analysis import calculate_score_differential, flatten_results
from data import get_combined_data
from html_parser import PlaywrightParser
from models import SportScores
import pandas as pd

sport_state_data = get_combined_data()

data: List[SportScores] = asyncio.run(PlaywrightParser().parse(sport_state_data))

print("")

flattened_data = flatten_results(data)
df = pd.DataFrame(flattened_data)
print("Base Data Frame")
print(df)
print("")

game_counts = df.groupby(["team_name", "sport"]).size().reset_index(name="game_count").sort_values("game_count", ascending=False)
print("Game Counts by Team and Sport")
print(game_counts)
print("")

pivoted_game_counts = game_counts.pivot(index="team_name", columns="sport", values="game_count")
print("Pivoted Game Counts by Team and Sport")
print(pivoted_game_counts)
print("")

pivoted_game_counts["total_games"] = pivoted_game_counts.sum(axis=1)
sorted_game_counts = pivoted_game_counts.sort_values("total_games", ascending=False)
print("Sorted Total Game Counts")
print(sorted_game_counts)
print("")

game_counts_by_state_and_sport = df.groupby(["state", "sport"]).size().reset_index(name="game_count").sort_values("game_count", ascending=False)
print("Game Counts by State and Sport")
print(game_counts_by_state_and_sport.to_string())
print("")


df["differential"] = df["score"].apply(calculate_score_differential)
print("Data Frame with Score Differential")
print(df)
print("")

print("Score Differential Total by Team and Sport")
differential_grouped = df.groupby(["team_name", "sport"]).agg(game_count=("differential", "size"), total_differential=("differential", "sum")).reset_index().sort_values("team_name")
print(differential_grouped)

