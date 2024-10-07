import requests
import schedule
import time
from datetime import datetime
import sqlite3
from dotenv import load_dotenv
import os


def api_url_constructor(city: str) -> tuple[str, str]:
    """
    Constructs the API URL for fetching weather data based on the provided city.

    Args:
        city (str): The name of the city for which weather data is requested.

    Returns:
        tuple: A tuple containing the constructed API URL and the API key.
            - API_URL (str): The complete URL for querying weather data.
            - API_KEY (str): The API key required for authentication.
    """
    load_dotenv()
    API_KEY = os.environ.get('API_KEY') # Task 0 .Replace with your API key
    your_city = city
    API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={your_city}&appid={API_KEY}&units=metric'
    return API_URL, API_KEY


def fetch_weather_data(API_URL: str, API_KEY: str, city: str) -> None:
    """
    Fetches weather data from the specified API URL, processes it, and adds it to the database.

    Args:
        API_URL (str): The complete URL for querying weather data.
        API_KEY (str): The API key required for authentication.
        city (str): The name of the city for which weather data is requested.

    """

    response = requests.get(API_URL.format(API_KEY))
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'timestamp': datetime.now().isoformat(),
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
        }
        print(weather_data)

        conn = sqlite3.connect('openweathermap.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO weather (city, timestamp, temperature, humidity, weather) VALUES (?, ?, ?, ?, ?)', 
                   (city, weather_data['timestamp'], weather_data['temperature'], weather_data['humidity'], weather_data['weather']))
        conn.commit()
        conn.close()
        print(f"weather data added successfully.")
        

# Create sqlite table
def create_table() -> None:
    """
    Creates an SQLite table to store weather data.

    The table schema includes columns for city, timestamp, temperature, humidity, and weather.

    """
    conn = sqlite3.connect('openweathermap.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        city TEXT, NOT NULL
        timestamp DATE NOT NULL,
        temperature REAL,
        humidity INTEGER,
        weather TEXT,
        PRIMARY KEY (timestamp)
    )
    ''')
    conn.commit()
    conn.close()


def main() -> None:
    """
    Main function to set up weather data fetching and scheduling.

    1. Creates the weather table in the database.
    2. Asks the user for the city (Hong Kong/New York/Tokyo).
    3. Constructs the API URL and retrieves the API key.
    4. Sets the data fetching interval (default is 1 minute).
    5. Schedules the weather data fetching job.
    6. Runs the scheduler indefinitely.
    """
    create_table()
    city = input("Enter the city (Hong Kong/New York/Tokyo): ")
    API_URL, API_KEY = api_url_constructor(city)
    interval = input("Enter the interval in minutes (default is 1): ")
    interval = int(interval) if interval.isdigit() else 1

    schedule.every(interval).minutes.do(fetch_weather_data(API_URL, API_KEY, city))
    
    print(f"Scheduler started. Fetching weather data every {interval} minute(s).")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()