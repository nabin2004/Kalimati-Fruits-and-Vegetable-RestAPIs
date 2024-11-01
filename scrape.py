from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Run in headless mode if desired

# Set up the Firefox service with the driver manager
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# URL to be scraped
url = 'https://kalimatimarket.gov.np/price'
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to be ready
date = driver.find_element(By.CSS_SELECTOR, "h4.bottom-head")
# Extract the table data
data = []
table = driver.find_element(By.ID, "commodityPriceParticular")
rows = table.find_elements(By.TAG_NAME, "tr")

# Loop through the rows and extract data
for row in rows[:]:  # Skip the header row
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols:
        # Get the text from each cell
        commodity = cols[0].text
        unit = cols[1].text
        min_price = cols[2].text
        max_price = cols[3].text
        avg_price = cols[4].text
        data.append({
            "Commodity": commodity,
            "Unit": unit,
            "Min Price": min_price,
            "Max Price": max_price,
            "Avg Price": avg_price
        })

# Close the WebDriver
driver.quit()

# Create a DataFrame for better visualization
df = pd.DataFrame(data)
print(df)
print(date)
# Optionally, save the data to a CSV file
df.to_csv(f'commodity_prices.csv', index=False)
