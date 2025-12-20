# Day 1: Match Dataset Cleaning

#------------- GET DATASET FROM KAGGLE HUB -----------
import kagglehub
path = kagglehub.dataset_download("martj42/international-football-results-from-1872-to-2017")
#------------- GET DATASET FROM KAGGLE HUB -----------

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

results = pd.read_csv(f"{path}/results.csv")

print()
print("Dropping NaN values from Result...")
results = results.dropna()

# keep only the required columns
print("Dropping unnecessary columns from Result...")
results = results[['date', 'home_team', 'away_team', 'home_score', 'away_score']]


# Add New Column 'Result' that shows whether Home Win, Away Win or Draw
# np.where(condition, value_if_true, value_if_false)
print("Adding new column 'Result'...")
results.insert(5, 'Result', np.where(results['home_score'] > results['away_score'], 'Home Win', np.where(results['home_score'] < results['away_score'], 'Away Win', 'Draw')))

# dropping rows with date less than 2025
# first converting to Dtype to datetime from object
print("Dropping rows with Date less than 2025...")
results['date'] = pd.to_datetime(results['date'])

# drop using boolean indexing
results = results[results['date'].dt.year >= 2025]

print("Dropping duplicate (home_team, away_team) pairs...")
results.drop_duplicates(subset=['home_team', 'away_team'], inplace=True, keep=False)
print()

# Creating a new DataFrame 'points' that shows each Team's performance
# based on Matches Played, Wins, Draws, Losses, and Points
print("\nCreating new dataFrame 'points'...\n")
teams = pd.concat(objs=[results['home_team'], results['away_team']], ignore_index=True).unique()
new_dictionary = []

for x in teams:
    # count home matches
    home = results[results['home_team'] == x]

    #count away matches
    away = results[results['away_team'] == x]

    #count total matches
    total_match = len(home) + len(away)

    #count wins, losses, and draws
    wins = len(home[home['Result'] == 'Home Win']) + len(away[away['Result'] == 'Away Win'])
    losses = len(away[away['Result'] == 'Home Win']) + len(home[home['Result'] == 'Away Win'])
    draws =  total_match - wins - losses

    points = wins * 3 + draws * 1

    # ----------CHECK-------------
    # if x == 'Mexico':
    #     print(home.columns)
    #     print(total_match)
    #     print(wins)
    #     print(losses)
    #     print(draws)
    #     print(points)

    #     print(new_dictionary[0:3])
    # ----------CHECK-------------

    new_dictionary.append({
        'Team': x,
        'Matches Played': total_match,
        'Wins': wins,
        'Draws': draws,
        'Losses': losses,
        'Points': points,
    })


points = pd.DataFrame(new_dictionary)
print(points)

points.sort_values(by=['Points'], inplace=True, ascending=False)

print("\n\nAdding 'Rank' column to Points...")
points.insert(loc=6, column='Rank', value=np.arange(start=1, stop=len(points)+1))

# ================= Analyzing Data=================

# Who performs better at home?
print("\nAnalyzing Home and Away Wins Percentage for each Team...")
analyze = []
for x in points['Team']:
    home_wins = len(results[(results['home_team'] == x) & (results['Result'] == 'Home Win')])
    away_wins = len(results[(results['away_team'] == x) & (results['Result'] == 'Away Win')])

    home_matches = len(results[results['home_team'] == x])
    if home_matches == 0:
        home_win_percent = np.nan
    else:
        home_win_percent = home_wins / home_matches * 100

    away_matches = len(results[results['away_team'] == x])
    if away_matches == 0:
        away_win_percent = np.nan
    else:
        away_win_percent = away_wins / away_matches * 100

    # ----------CHECK-------------
    # if x == 'Mexico':
    #     print(results[results['home_team'] == x])
    #     print('=' * 60)
    #     print(results[results['away_team'] == x])
    #     print('=' * 60)
    #     print(home_wins)
    #     print(away_wins)
    #     print(home_win_percent)
    #     print(away_win_percent)
    # ----------CHECK-------------

    analyze.append({
        'Team': x,
        'Home Wins': home_wins,
        'Away Wins': away_wins,
        'Home Win (%)': home_win_percent,
        'Away Win (%)': away_win_percent
    })

answer = pd.DataFrame(analyze)
answer.dropna(inplace=True)
answer = answer.round(2)

better_at_home = answer[answer['Home Win (%)'] > answer['Away Win (%)']]
teams_better_at_home = pd.Series(better_at_home['Team'])

print()
print('*' * 60)
print(f"{len(better_at_home)} Teams better at Home Matches:")
print('*' * 60)
print(teams_better_at_home.values)
print()

better_at_away = answer[answer['Home Win (%)'] < answer['Away Win (%)']]
teams_better_at_away = pd.Series(better_at_away['Team'])

print()
print('*' * 60)
print(f"{len(better_at_away)} Teams better at Away Matches:")
print('*' * 60)
print(teams_better_at_away.values)
print()

equal_home_away = answer[answer['Home Win (%)'] == answer['Away Win (%)']]
teams_equal_home_away = pd.Series(equal_home_away['Team'])

print()
print('*' * 60)
print(f"{len(equal_home_away)} Teams equally good at Home & Away Matches:")
print('*' * 60)
print(teams_equal_home_away.values)
print()

# ================= PLOTTING =================

plt.figure(figsize=(10, 6))

plt.plot(answer[answer['Team'].isin(teams_better_at_home)]['Home Win (%)'], answer[answer['Team'].isin(teams_better_at_home)]['Away Win (%)'], 'o', mfc='m', mec='m', label='Better at Home')
plt.plot(answer[answer['Team'].isin(teams_better_at_away)]['Home Win (%)'], answer[answer['Team'].isin(teams_better_at_away)]['Away Win (%)'], '^', mfc='c', mec='c', label='Better at Away')
plt.plot(answer[answer['Team'].isin(teams_equal_home_away)]['Home Win (%)'], answer[answer['Team'].isin(teams_equal_home_away)]['Away Win (%)'], 's', mfc='r', mec='r', label='Equal at Both')
plt.plot([-10, 119], [-10, 119], c='gray', lw=1, ls='dashed')

font1 = {'family':'serif','color':'maroon','size':20}
font2 = {'family':'serif','color':'k','size':12}

plt.title('Home Vs Away Win Chart', fontdict = font1)
plt.xlabel('Home Wins in %', fontdict = font2)
plt.ylabel('Away Wins in %', fontdict = font2)

plt.legend(loc='best', fontsize=8)

plt.show()

plt.figure(figsize=(10, 8))

colors = cm.tab20c(np.linspace(0, 1, 15))
plt.barh(y=points[0:15]['Team'], width=points[0:15]['Points'], height=0.7, color=colors)
plt.xlabel('Points', fontdict=font2)
plt.ylabel('Teams', fontdict=font2)
plt.title('15 Highest Points', fontdict=font1)

plt.show()
