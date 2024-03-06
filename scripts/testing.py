import pandas as pd

data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
index = ['row1', 'row2', 'row3']

df = pd.DataFrame(data, index=index)
print(df)

# Add a new column 'D' with values [10, 11, 12]
df['D'] = [10, 11, 12]

# Add a new row with index 'row4' and values for columns A, B, C, and D
df.loc['row4'] = [13, 14, 15, 16]

print(df)