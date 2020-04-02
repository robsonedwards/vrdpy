import pandas as pd
import os
from collections import defaultdict

# Load VRD data
paths = os.listdir()
paths = [path for path in paths if path[-4:] == ".csv"]
dfs = [pd.read_csv(s) for s in paths]
for df in dfs:
    for col in df:
        df[col] = df[col].str.lower().str.strip()

# gets the location (x,y) of the i'th pick in snake draft [(0, 0) to (7, 44)]
# for i = 0, 1, ... 359
def get_index(i, n_players):
    row = i // n_players
    col = i % n_players 
    if row % 2:
        return (row, n_players - 1 - col)
    else:
        return (row, col)

# Find data by card
cards = defaultdict(list)
for df in dfs:
    n_players = df.shape[1]
    for i in range(df.size):
        cardname = df.iloc[get_index(i, n_players)]
        cards[cardname].append(i)

cards_list = []
for card, ls in cards.items():
    cards_list.append([card, min(ls) + 1, round(sum(ls) / len(ls) + 1, 2)])
# Sort by min pick #
cards_list = sorted(cards_list, key = lambda x : x[1])
# then sort by average pick #
cards_list = sorted(cards_list, key = lambda x : x[2])

cards_df = pd.DataFrame(cards_list, columns=["cardname","min","mean"])
cards_df.to_csv("out.csv")
