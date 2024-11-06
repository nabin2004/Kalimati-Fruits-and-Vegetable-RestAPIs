from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

# Set up Firefox options
options = Options()
options.add_argument("--headless")  

# Set up the Firefox service with the driver manager
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# URL to be scraped
url = 'https://kalimatimarket.gov.np/price'
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

# Wait until the preloader disappears
try:
    WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, "preloader")))
except:
    print("Preloader took too long to disappear")

# Set the date to "2024-11-05"
specify_date = '2024-11-05'
date_input = driver.find_element(By.ID, "datePricing")
driver.execute_script(f"arguments[0].value = '{specify_date}';", date_input)

# Click the "Check Prices" button
submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn-theme.comment-btn")
submit_button.click()

# Wait for the table to load after submission
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commodityPriceParticular")))

# Extract the date displayed on the page
date = driver.find_element(By.CSS_SELECTOR, "h4.bottom-head").text

# Extract the table data
data = []
table = driver.find_element(By.ID, "commodityPriceParticular")
rows = table.find_elements(By.TAG_NAME, "tr")

# Loop through the rows and extract data
for row in rows:
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

# Convert data to DataFrame and add date
df = pd.DataFrame(data)
df["Date"] = date

# Save the data to a CSV file with specify_date as the filename
df.to_csv(f'data/commodity_prices_{specify_date}.csv', index=False)

print(df)
