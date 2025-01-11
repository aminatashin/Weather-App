# Weather App

This is a simple weather app that retrieves real-time weather data from the OpenWeatherMap API. It supports both current weather data and 5-day forecasts. The app also includes CRUD functionality to store, update, retrieve, and delete weather data using a SQLite database.

---

## Features
1. **Real-Time Weather**:
   - Fetch current weather data for any location.
   - Fetch a 5-day weather forecast.

2. **CRUD Functionality**:
   - Save weather data for specific locations to a database.
   - Retrieve saved weather data.
   - Update saved weather records.
   - Delete weather records.

3. **Frontend**:
   - Simple UI built with HTML, CSS, and JavaScript.

4. **API Integration**:
   - Utilizes OpenWeatherMap API for real-time weather data.

---

## Endpoints
### **Backend API**
- `/`:
  - Displays a welcome message and instructions for using the app.
- `/weather?location=<city>`:
  - Fetches the current weather for the specified city.
  - Example: `/weather?location=Seattle`.
- `/forecast?location=<city>`:
  - Fetches a 5-day weather forecast for the specified city.
  - Example: `/forecast?location=Seattle`.
- `/save-weather` (POST):
  - Saves weather data for a location to the database.
  - Example JSON payload:
    ```json
    {
      "location": "Seattle",
      "date_range": "2025-01-01 to 2025-01-07",
      "weather_info": "{\"temp\": 5, \"condition\": \"Cloudy\"}"
    }
    ```
- `/get-weather-data` (GET):
  - Retrieves all saved weather data from the database.
- `/update-weather/<id>` (PUT):
  - Updates a specific weather record in the database.
  - Example JSON payload:
    ```json
    {
      "weather_info": "{\"temp\": 10, \"condition\": \"Sunny\"}"
    }
    ```
- `/delete-weather/<id>` (DELETE):
  - Deletes a specific weather record from the database.

---

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aminatashin/Weather-App.git
   cd Weather-App
