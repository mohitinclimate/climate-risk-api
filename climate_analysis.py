import pandas as pd
import matplotlib.pyplot as plt

# Download climate temperature data
url = "https://raw.githubusercontent.com/datasets/global-temp/master/data/annual.csv"

# Load the dataset
df = pd.read_csv(url)

# Print column names and first few rows
print("Column names in the dataset:", df.columns)
print(df.head())

# ✅ Use 'Year' instead of 'Date' since 'Date' does NOT exist
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# ✅ Rename 'Year' to 'Date' so the rest of the code works
df.rename(columns={'Year': 'Date'}, inplace=True)

# ✅ Filter data from 1900 onwards
df = df[df['Date'].dt.year >= 1900]

# ✅ Plot the graph
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Mean'], label='Global Temperature Anomaly (°C)', color='red')
plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Temperature Anomaly (°C)')
plt.title('Global Temperature Change Over Time')
plt.legend()
plt.grid()
plt.show()
