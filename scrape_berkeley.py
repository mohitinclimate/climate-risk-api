from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Step 1: Set up Selenium WebDriver
chrome_driver_path = "./chromedriver.exe"  # Ensure this is in the same folder as your script
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs Chrome in the background
driver = webdriver.Chrome(service=service, options=options)

# Step 2: Open the Berkeley Earth webpage
url = "https://berkeleyearth.org/data/"
driver.get(url)

# Step 3: Wait for the page to fully load (important for JavaScript-based tables)
time.sleep(5)  # Adjust if needed

# Step 4: Find the data table
tables = driver.find_elements(By.TAG_NAME, "table")

if tables:
    data = []
    headers = [header.text.strip() for header in tables[0].find_elements(By.TAG_NAME, "th")]

    # Extract rows
    for row in tables[0].find_elements(By.TAG_NAME, "tr")[1:]:  # Skip header row
        values = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
        if values:
            data.append(values)

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Save to CSV
    df.to_csv("India_Temperature_Data.csv", index=False)
    print("✅ Data successfully extracted and saved as 'India_Temperature_Data.csv'!")

else:
    print("❌ No tables found on the page. The page might have a different structure.")

# Close the browser
driver.quit()
