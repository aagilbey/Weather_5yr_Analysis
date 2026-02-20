README - How to run program

Overview
    This project retrieves historical weather data for a specified location and week-long date range, calculates 5-year
    averages, and visualizes temperature, wind speed, and precipitation trends. It provides a simple way to understand
    how the weather behaved on specific dates over the past five years.

    The project demonstrates:
        -API data retrieval
        -Data aggregation and analysis
        -Database storage using SQLite
        -Visualization through Matplotlib
        -Python classes


Usage
    1. Configure location and starting date:
            wd = WeatherData(
                latitude =
                longitude =
                month =
                day =
                year =
            )

    2. Fetch weekly 5 year weather statistics:
            wd.get_week_stats()

    3. Store data in SQLite

    4. Visualize data

Outputs Produced
    Weather Data Visualization
        Examples:
            -Average Temperature over a week
            -Average Precipitation over a week
            -Average Wind Speed over a Week

Files Included
    - main.py: Main program script
    - test.py: Tests methods in main.py
    - weather.db: SQLite database (generates once code is ran)
    - requirements.txt: Packaged and modules used
    - readme.txt