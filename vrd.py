import pandas as pd
import os
from collections import defaultdict
from levenshtein import levenshtein

# Load VRD data
paths = os.listdir("data")
paths = ["data/" + path for path in paths if path[-4:] == ".csv"]
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

# Check for misspellings/duplicates
CHECK_FOR_DUPLICATES = False
if(CHECK_FOR_DUPLICATES):
    for i in range(len(cards_list)):
        for j in range(i + 1, len(cards_list)):
            card1 = cards_list[i][0]
            card2 = cards_list[j][0]
            d = levenshtein(card1, card2)
            if d < 3:
                print("".join(["Warning! Cards ", card1, " and ",
                    card2, " may be misspellings of the same card!"]))

# Sort by min pick #
cards_list = sorted(cards_list, key = lambda x : x[1])
# then sort by average pick #
cards_list = sorted(cards_list, key = lambda x : x[2])

cards_df = pd.DataFrame(cards_list, columns=["cardname","min","mean"])
cards_df.to_csv("out.csv")
