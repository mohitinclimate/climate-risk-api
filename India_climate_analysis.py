import pandas as pd

# Load the dataset from the CSV file
df = pd.read_csv("annual-temperature-anomalies.csv")

# Preview the columns and first few rows to understand the structure
print(df.columns)
print(df.head())

# Filter the data for India and for the global average (World)
india_data = df[df['Entity'] == 'India']
global_data = df[df['Entity'] == 'World']

# Set the year as index (optional, for easier plotting or alignment)
india_data.set_index('Year', inplace=True)
global_data.set_index('Year', inplace=True)

# Print the last few records to see recent anomalies for India vs. World
print("India Temperature Anomalies (tail):")
print(india_data.tail())
print("\nGlobal Temperature Anomalies (tail):")
print(global_data.tail())
