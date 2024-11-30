from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.responses import JSONResponse

app = FastAPI()

# Load CSV data
data_file = "data/data.csv"

try:
    data = pd.read_csv(data_file)
except FileNotFoundError:
    raise RuntimeError("CSV file not found. Please make sure 'data.csv' exists.")

# Preprocess Date column to ensure proper comparisons
data['Date'] = data['Date'].str.strip()

@app.get("/")
def read_root():
    """
    Root Endpoint of the API.

    This is the base route for the API. When accessed, it returns a simple 
    message indicating that the user has successfully accessed the API.

    **Response:**
    - 200 OK: Returns a JSON object with a greeting message.
    - Example:
      ```json
      {
        "message": "Welcome to the Commodity Price API!"
      }
      ```

    **Usage Example:**
    ```
    GET / 
    ```

    **Notes:**
    - This endpoint is used for testing the availability of the API.
    """
    return {"message": "Welcome to the Commodity Price API!"}

@app.get("/commodities/")
def get_commodities():
    """
    Retrieve All Commodities Data.

    This endpoint returns a list of all commodities along with their prices and other
    details (e.g., minimum price, maximum price, average price, and date) in the dataset.
    The data is returned in JSON format, where each commodity's details are represented
    as a dictionary.

    **Response:**
    - 200 OK: A list of commodities with details in JSON format.
    - Example:
      ```json
      [
        {
          "Commodity": "Wheat",
          "Unit": "KG",
          "Min_Price": 100,
          "Max_Price": 120,
          "Avg_Price": 110,
          "Date": "2024-11-01"
        },
        {
          "Commodity": "Rice",
          "Unit": "KG",
          "Min_Price": 80,
          "Max_Price": 95,
          "Avg_Price": 87,
          "Date": "2024-11-01"
        }
      ]
      ```

    **Usage Example:**
    ```
    GET /commodities/
    ```

    **Notes:**
    - This endpoint is useful for retrieving all commodity data available in the system.
    """
    return data.to_dict(orient="records")

@app.get("/commodities/{commodity_name}")
def get_commodity_by_name(commodity_name: str):
    """
    Retrieve Details of a Specific Commodity by Name.

    This endpoint retrieves the data for a specific commodity based on its name.
    The query parameter `commodity_name` is used to filter the dataset. If the 
    commodity is not found in the data, a 404 error will be raised.

    **Parameters:**
    - `commodity_name` (path parameter): The name of the commodity you want to retrieve.

    **Response:**
    - 200 OK: A list of commodities matching the given name with detailed information.
    - 404 Not Found: If no matching commodity is found.
    - Example (200 OK):
      ```json
      [
        {
          "Commodity": "Wheat",
          "Unit": "KG",
          "Min_Price": 100,
          "Max_Price": 120,
          "Avg_Price": 110,
          "Date": "2024-11-01"
        }
      ]
      ```

    **Usage Example:**
    ```
    GET /commodities/Wheat
    ```

    **Notes:**
    - The search is case-insensitive and can handle partial matches using the `contains` method.
    - This endpoint helps you retrieve specific commodity data when you know the commodity's name.
    """
    filtered_data = data[data["Commodity"].str.contains(commodity_name, na=False)]
    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="Commodity not found")
    return filtered_data.to_dict(orient="records")

@app.get("/commodities/avg_price_range/")
def get_commodities_in_avg_price_range(min_avg: float, max_avg: float):
    """
    Retrieve Commodities within a Specific Average Price Range.

    This endpoint allows users to query commodities based on the average price range.
    The user needs to provide a `min_avg` and `max_avg` as query parameters. 
    The response will contain all commodities whose average price lies between the specified range.

    **Parameters:**
    - `min_avg` (query parameter): The minimum average price of the commodities to be retrieved.
    - `max_avg` (query parameter): The maximum average price of the commodities to be retrieved.

    **Response:**
    - 200 OK: A list of commodities that fall within the specified price range.
    - 404 Not Found: If no commodities are found within the given price range.
    - Example (200 OK):
      ```json
      [
        {
          "Commodity": "Wheat",
          "Unit": "KG",
          "Min_Price": 100,
          "Max_Price": 120,
          "Avg_Price": 110,
          "Date": "2024-11-01"
        }
      ]
      ```

    **Usage Example:**
    ```
    GET /commodities/avg_price_range/?min_avg=90&max_avg=120
    ```

    **Notes:**
    - This endpoint can be useful when analyzing commodities based on their price ranges.
    """
    filtered_data = data[(data["Avg_Price"] >= min_avg) & (data["Avg_Price"] <= max_avg)]
    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="No commodities found in the given price range")
    return filtered_data.to_dict(orient="records")

@app.get("/commodities/by_date/")
def get_commodities_by_date(date: str):
    """
    Retrieve Commodities for a Specific Date.

    This endpoint retrieves all commodities that were recorded on a particular date.
    The user provides a `date` parameter in the query string. The endpoint will filter
    the commodities based on the provided date and return all matching records.

    **Parameters:**
    - `date` (query parameter): The specific date for which commodities are to be retrieved (in `YYYY-MM-DD` format).

    **Response:**
    - 200 OK: A list of commodities recorded on the specified date.
    - 404 Not Found: If no commodities are found for the given date.
    - Example (200 OK):
      ```json
      [
        {
          "Commodity": "Rice",
          "Unit": "KG",
          "Min_Price": 80,
          "Max_Price": 95,
          "Avg_Price": 87,
          "Date": "2024-11-01"
        }
      ]
      ```

    **Usage Example:**
    ```
    GET /commodities/by_date/?date=2024-11-01
    ```

    **Notes:**
    - This endpoint helps when you need commodity data for a specific date, which can be useful for trend analysis or historical price reviews.
    """
    filtered_data = data[data["Date"] == date]
    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="No commodities found for the given date")
    return filtered_data.to_dict(orient="records")
