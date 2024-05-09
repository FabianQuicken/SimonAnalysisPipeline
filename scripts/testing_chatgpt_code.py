import pandas as pd
import numpy as np

# Existing DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# New array to add as a column
new_data = [10, 20, 30, 40]  # Array length is 4, while DataFrame index length is 3

# Reindex the DataFrame with a new index matching the length of new_data
df = df.reindex(range(len(new_data)))

# Assign the new array as a new column
df['C'] = new_data

print(df)
