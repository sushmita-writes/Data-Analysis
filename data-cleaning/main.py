import numpy as np
import pandas as pd

initial_data = pd.read_csv('./dirty_sports_match_dataset_1500_rows.csv')

print('=' * 30)
print("Step 1: Drop Missing Values")
print('=' * 30)
print("Initial missing values count:")
print('-' * 30)
print(initial_data.isna().sum())
print()
new_data = initial_data.dropna(subset = ['Home Score', 'Away Score']).copy()
print("After:")
print('-' * 30)
print(new_data.isna().sum())
print()

print('=' * 30)
print("Step 2: Convert Home Score and Away Score to Numeric")
print('=' * 30)
new_data.loc[:, ['Home Score', 'Away Score']] = new_data[['Home Score', 'Away Score']].replace({
    'Two': '2',
    'Three': '3'
})

new_data['Home Score'] = pd.to_numeric(new_data['Home Score'])
new_data['Away Score'] = pd.to_numeric(new_data['Away Score'])
print(new_data.dtypes)
print()

print('=' * 30)
print("Step 3: Correct Wrong Values in Result")
print('=' * 30)
new_data.loc[:, 'Result'] = np.where(new_data['Home Score'] > new_data['Away Score'], 'Home Win', np.where(new_data['Home Score'] < new_data['Away Score'], 'Away Win', 'Draw'))
print(new_data['Result'].value_counts())
print()


print('=' * 30)
print("Step 4: Clean Wrong Format Data in 'Match Date'")
print('=' * 30)
print("\nBefore Cleaning:")
print('-' * 30)
print(new_data.loc[1435:1440, 'Match Date'])

print("\nAfter Cleaning:")
print('-' * 30)
new_data['Match Date'] = pd.to_datetime(new_data['Match Date'], format='mixed')
print(new_data.loc[1435:1440, 'Match Date'])
print()
