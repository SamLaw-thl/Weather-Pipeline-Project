import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re


def fetch_data_from_db(city: str, starting_date: str, ending_date: str) -> pd.DataFrame | None:
    """
    Fetches weather data from the SQLite database for further analysis.

    Args:
        city (str): The name of the city for which weather data is requested.
        starting_date (str): The start date (in ISO format, e.g., '2024-10-01') for the data retrieval.
        ending_date (str): The end date (in ISO format, e.g., '2024-10-07') for the data retrieval.

    Returns:
        pd.DataFrame or None: A DataFrame containing weather data columns (city, timestamp, temperature, humidity, weather).
            If no data is found for the specified city and date range, returns None.
    """
    conn = sqlite3.connect('openweathermap.db')
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM weather WHERE city = ? and timestamp BETWEEN ? AND ?", (city, starting_date, ending_date)
        )
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    if rows:
        df = pd.DataFrame(rows)
        df.columns = ['city', 'timestamp', 'temperature', 'humidity', 'weather']
    
        return df
    else:
        return None


# Print weather data given table_name
def print_weather_data(city: str, starting_date: str, ending_date: str) -> None:
    """
    Prints weather data from the SQLite database for the specified city and date range.

    Args:
        city (str): The name of the city for which weather data is requested.
        starting_date (str): The start date (in ISO format, e.g., '2024-10-01') for data retrieval.
        ending_date (str): The end date (in ISO format, e.g., '2024-10-07') for data retrieval.

    """
    df = fetch_data_from_db(city, starting_date, ending_date)
    print(df)



def timestamp_spliter(starting_time: str, ending_time: str, split: int = 10) -> list[str]:
    """
    Splits the timestamp range between starting_time and ending_time into evenly distributed intervals.

    Args:
        starting_time (str): The start timestamp (in ISO format, e.g., '2024-10-01T10:00:00').
        ending_time (str): The end timestamp (in ISO format, e.g., '2024-10-01T18:00:00').
        split (int, optional): The number of evenly distributed intervals. Defaults to 10.

    Returns:
        List[str]: A list of ISO-formatted timestamps representing the evenly split intervals.
    """
    # convert the str into timestamps
    starting_time = datetime.strptime(starting_time, "%Y-%m-%dT%H:%M:%S")
    ending_time = datetime.strptime(ending_time, "%Y-%m-%dT%H:%M:%S")

    # calculate total duration 
    total_duration = ending_time - starting_time

    # calculate the length of each split duration
    split_duration = total_duration/split

    # Generate split timestamps
    split_timestamps_list = []
    current_time = starting_time
    for _ in range(split):
        split_timestamps_list.append(current_time.isoformat())
        current_time += split_duration

    return split_timestamps_list


def timestamp_converter(split_timestamps_list: list[str]) -> list[str]:
    """
    Converts a list of split timestamps (in ISO format) to a simplified list containing only hour and minute.

    Args:
        split_timestamps_list (List[str]): A list of ISO-formatted timestamps.

    Returns:
        List[str]: A list of simplified timestamps (hour:minute).
    """

    simplified_split_timestamps_list =[]
    for timestamps in split_timestamps_list:
        pattern = r'(\d{2}:\d{2})'
        match = re.search(pattern, timestamps)
        if match:
            simplified_split_timestamps_list.append(match.group(1)) 
    
    return simplified_split_timestamps_list
        

def temperature_trends_graph(city: str, starting_date: str, ending_date: str) -> None:
    """
    Plots a graph comparing min, mean, and max temperatures for the specified city.

    Args:
        city (str): The name of the city for which weather data is requested.
        starting_date (str): The start date (in ISO format, e.g., '2024-10-01') for data retrieval.
        ending_date (str): The end date (in ISO format, e.g., '2024-10-07') for data retrieval.
    """
    df = fetch_data_from_db(city, starting_date, ending_date)
    df['date'] = pd.to_datetime(df['timestamp'])

    # Set the timestamp column as the index
    df.set_index('date', inplace=True)

    temperature_per_hr_max = df['temperature'].resample('h').max()
    temperature_per_hr_mean = df['temperature'].resample('h').mean()
    temperature_per_hr_min = df['temperature'].resample('h').min()

    plt.plot(temperature_per_hr_min, label='Min Temperature', color='blue')
    plt.plot(temperature_per_hr_mean, label='Mean Temperature', color='green')
    plt.plot(temperature_per_hr_max, label='Max Temperature', color='red')
    plt.legend()
    plt.xlabel('Time (Hourly)')
    plt.ylabel('Temperature (°C)')

    split_timestamps_list = timestamp_spliter(starting_date, ending_date)
    simplified_split_timestamps_list = timestamp_converter(split_timestamps_list)
    plt.xticks(split_timestamps_list, simplified_split_timestamps_list)

    plt.title('Temperature Trends')
    plt.tight_layout()
    plt.show()



def mean_temperature_per_hr_comp_diff_city(starting_date: str, ending_date: str) -> None:
    """
    Plots a graph comparing mean temperatures per hour for Hong Kong, New York, and Tokyo.

    Args:
        starting_date (str): The start date (in ISO format, e.g., '2024-10-01') for data retrieval.
        ending_date (str): The end date (in ISO format, e.g., '2024-10-07') for data retrieval.
    """

    df_hk = fetch_data_from_db('Hong Kong', starting_date, ending_date)
    df_hk['date'] = pd.to_datetime(df_hk['timestamp'])

    df_ny = fetch_data_from_db('New York', starting_date, ending_date)
    df_ny['date'] = pd.to_datetime(df_ny['timestamp'])

    df_tyo = fetch_data_from_db('Tokyo', starting_date, ending_date)
    df_tyo['date'] = pd.to_datetime(df_tyo['timestamp'])

    # Set the timestamp column as the index
    df_hk.set_index('date', inplace=True)
    df_ny.set_index('date', inplace=True)
    df_tyo.set_index('date', inplace=True)

    temperature_per_hr_mean_hk = df_hk['temperature'].resample('h').mean()
    temperature_per_hr_mean_ny = df_ny['temperature'].resample('h').mean()
    temperature_per_hr_mean_tyo = df_tyo['temperature'].resample('h').mean()

    plt.plot(temperature_per_hr_mean_hk, label='Hong Kong Mean Temperature', color='blue')
    plt.plot(temperature_per_hr_mean_ny, label='New York Mean Temperature', color='green')
    plt.plot(temperature_per_hr_mean_tyo, label='Tokyo Mean Temperature', color='red')    

    plt.legend()
    plt.xlabel('Time (Hourly)')
    plt.ylabel('Temperature (°C)')

    split_timestamps_list = timestamp_spliter(starting_date, ending_date)
    simplified_split_timestamps_list = timestamp_converter(split_timestamps_list)
    plt.xticks(split_timestamps_list, simplified_split_timestamps_list)

    plt.title('Temperature Trends')
    plt.tight_layout()
    plt.show()

# e.g. mean_temperature_per_hr_comp_diff_city('2024-08-28T11:00:00', '2024-08-28T16:00:00')



