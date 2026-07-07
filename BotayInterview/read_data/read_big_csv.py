import pandas as pd

chunk_size = 10000
total_sum = 0
count = 0

for chunk in pd.read_csv("large_file.csv", chunksize=chunk_size):
    total_sum += chunk["value"].sum()
    count += len(chunk)

mean_value = total_sum / count
print(f"Mean value: {mean_value}")