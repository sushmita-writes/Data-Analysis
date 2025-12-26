# Sports Match Dataset - Data Cleaning

Data cleaning using Python, Pandas, NumPy, and Matplotlib to clean and analyze a dirty sports match dataset.

**Input**: [Dirty dataset](./dirty_sports_match_dataset_1500_rows.csv)
**Output**: [Clean dataset](./cleaned_sports_match_dataset.csv)

## Steps Involved

1. **Dropped missing values** in Home Score and Away Score columns
2. **Converted text to numeric** (replaced 'Two' → 2, 'Three' → 3)
3. **Corrected wrong values** in Result column based on actual scores
4. **Fixed date formats** using mixed format parsing
5. **Normalized string data** (stripped whitespace, title case)
6. **Analyzed numerical data** using statistical descriptions
7. **Detected outliers** using box plots
8. **Exported cleaned data** to CSV
