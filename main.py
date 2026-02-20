
# All imports
import requests
import matplotlib.pyplot as plt
from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date, timedelta


#Stores all weather data
class WeatherData:
    def __init__(self, latitude, longitude, month, day, year):

        # Location and date
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = year

        #Dates
        self.dates = []

        # Temperature
        self.avg_temp = []
        self.min_temp = []
        self.max_temp = []

        # Wind speed
        self.avg_wind_speed = []
        self.min_wind_speed = []
        self.max_wind_speed = []

        # Precipitation
        self.sum_precipitation = []
        self.min_precipitation = []
        self.max_precipitation = []



    def get_5yr_stats_for_date(self, month, day):
        """
        Retrieves weather data from Open-Meteo API for provided month, day and year across 5 consecutive years
        and calculates average, minimum, and maximum temperature, wind speed and precipitation before storing in
        a dictionary.

        Args:
            month (int): Month to retrieve data for
            day (int): Day to retrieve data for

        Returns:
            dict: Weather data
        """
        temps, wind_speeds, precipitations = [], [], []

        for i in range(5): # Loop through 5 consecutive years
            year = self.year + i
            date_str = f"{year}-{month:02d}-{day:02d}"

            url = "https://archive-api.open-meteo.com/v1/archive"

            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "start_date": date_str,
                "end_date": date_str,
                "daily": "temperature_2m_mean,windspeed_10m_mean,precipitation_sum",
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": "auto"
            }

            # Retrieve weather data from API
            response = requests.get(url, params=params)
            data = response.json()

            # Appending temp, wind, precip data for specific year into respective list
            temps.append(data["daily"]["temperature_2m_mean"][0])
            wind_speeds.append(data["daily"]["windspeed_10m_mean"][0])
            precipitations.append(data["daily"]["precipitation_sum"][0])

        # Temperature Calculations
        avg_temp = sum(temps) / len(temps)
        min_temp = min(temps)
        max_temp = max(temps)

        # Wind Speed Calculations
        avg_wind_speed = sum(wind_speeds) / len(wind_speeds)
        min_wind_speed = min(wind_speeds)
        max_wind_speed = max(wind_speeds)

        # Precipitation Calculations
        sum_precipitation = sum(precipitations)
        min_precipitation = min(precipitations)
        max_precipitation = max(precipitations)

        # Create and populate dictionary avg, min, max weather data
        return {
                "avg_temp": avg_temp, "min_temp": min_temp, "max_temp": max_temp,
                "avg_wind_speed": avg_wind_speed, "min_wind_speed": min_wind_speed, "max_wind_speed": max_wind_speed,
                "sum_precip": sum_precipitation, "min_precip": min_precipitation, "max_precip": max_precipitation,
            }



    def get_week_stats(self, week_length=7):
        """
        Calculates 5 year weather statistics for each day in a week based on provided date and appends it
        to the dictionary created in get_5yr_stats_for_date.

        For each day in the week:
            -Calls get_5yr_stats_for_date to get average, min, max temperature, wind speed, and precipitation.
            -Appends results to instance lists.

        Params:
            week_length (int): Length of week to calculate statistics for

        Returns:
            None: Populates instance lists with weekly data
        """
        start_date = date(self.year, self.month, self.day)

        for i in range(week_length): # Loop through each day for one week
            current_date = start_date + timedelta(days=i)
            month = current_date.month
            day = current_date.day

            # Retrieve 5 year stats for each date
            stats = self.get_5yr_stats_for_date(month, day)

            # Store date
            self.dates.append(current_date.strftime("%m-%d"))
            # Populate all weekly data lists
            self.avg_temp.append(stats["avg_temp"])
            self.min_temp.append(stats["min_temp"])
            self.max_temp.append(stats["max_temp"])
            self.avg_wind_speed.append(stats["avg_wind_speed"])
            self.min_wind_speed.append(stats["min_wind_speed"])
            self.max_wind_speed.append(stats["max_wind_speed"])
            self.sum_precipitation.append(stats["sum_precip"])
            self.min_precipitation.append(stats["min_precip"])
            self.max_precipitation.append(stats["max_precip"])


# Location and Date Information
wd = WeatherData(
    latitude=42.35,
    longitude=-71.05,
    month=12,
    day=1,
    year=2010
)

wd.get_week_stats()

# Weather Data Table and Columns
Base = declarative_base()
class WeatherTable(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(String)  # store the date as "MM-DD"

    # Temperature fields
    avg_temp = Column(Float)
    min_temp = Column(Float)
    max_temp = Column(Float)

    # Wind speed fields
    avg_wind_speed = Column(Float)
    min_wind_speed = Column(Float)
    max_wind_speed = Column(Float)

    # Precipitation fields
    sum_precipitation = Column(Float)
    min_precipitation = Column(Float)
    max_precipitation = Column(Float)

# Connect to SQLite database file named 'weather.db' and creates table from 'WeatherTable' class
engine = create_engine('sqlite:///weather.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Delete existing rows to reset table
session.query(WeatherTable).delete()
session.commit()

# Populate Weather Table with data for each day in the week
for i in range(len(wd.dates)):
    day_stats = WeatherTable(
        latitude = wd.latitude,
        longitude = wd.longitude,
        date = wd.dates[i],
        avg_temp = wd.avg_temp[i],
        min_temp = wd.min_temp[i],
        max_temp = wd.max_temp[i],
        avg_wind_speed = wd.avg_wind_speed[i],
        min_wind_speed = wd.min_wind_speed[i],
        max_wind_speed = wd.max_wind_speed[i],
        sum_precipitation = wd.sum_precipitation[i],
        min_precipitation = wd.min_precipitation[i],
        max_precipitation = wd.max_precipitation[i]
    )
    session.add(day_stats)

session.commit()
session.close()

# Plot Info
rows = session.query(WeatherTable).all()
dates = [row.date for row in rows]
avg_temps = [row.avg_temp for row in rows]
avg_wind_speed = [row.avg_wind_speed for row in rows]
sum_precip = [row.sum_precipitation for row in rows]

# Average Temperature Plot
plt.plot(dates, avg_temps, marker='o')
plt.title("Week Long Average Temperature Across 5 Years")
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.show()

# Average Wind Speed Plot
plt.plot(dates, avg_wind_speed, marker='o')
plt.title("Week Long Average Wind Speed Across 5 Years")
plt.xlabel("Date")
plt.ylabel("Wind Speed (mph)")
plt.show()

# Total Precipitation Plot
plt.plot(dates, sum_precip, marker='o')
plt.title("Week Long Total Precipitation Across 5 Years")
plt.xlabel("Date")
plt.ylabel("Precipitation (Inches)")
plt.show()