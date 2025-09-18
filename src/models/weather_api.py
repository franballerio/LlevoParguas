import logging
import os
import openmeteo_requests
import pandas as pd
import requests_cache

from datetime import date, timedelta
from retry_requests import retry


def fetch_weather(today=False):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    tomorrow = date.today()

    if (not today):
        tomorrow = tomorrow + timedelta(days=1)

    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    # 2. Update your params dictionary
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -34.5926,
        "longitude": -58.4364,
        "hourly": ["temperature_2m", "precipitation", "precipitation_probability", "apparent_temperature", "cloud_cover", "visibility", "wind_speed_10m", "dew_point_2m", "relative_humidity_2m"],
        "current": ["temperature_2m", "precipitation", "apparent_temperature"],
        "timezone": "America/Argentina/Buenos_Aires",
        "start_date": tomorrow_str,
        "end_date": tomorrow_str,
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = int(current.Variables(0).Value())
    current_precipitation = current.Variables(1).Value()
    current_apparent_temperature = int(current.Variables(2).Value())

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(4).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(7).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(8).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["visibility"] = hourly_visibility
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["current_temperature_2m"] = current_temperature_2m
    hourly_data["current_precipitation"] = current_precipitation
    hourly_data["current_apparent_temperature"] = current_apparent_temperature

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    return hourly_dataframe

# Helper function to get a summary for a specific time period


def get_period_summary(df, start_hour, end_hour):
    period_df = df[df['date'].dt.hour.between(start_hour, end_hour)]
    if period_df.empty:
        return "N/A", "❔"

    # Calculate average temperature and cloud cover for the period
    temp = int(period_df['temperature_2m'].mean())
    cloud = period_df['cloud_cover'].mean()

    emoji = "☀️"
    if cloud > 65:
        emoji = "☁️"
    elif cloud > 30:
        emoji = "⛅️"

    return f"Around {temp}°C", emoji


def parse_weather(df):
    max_temp = int(df['temperature_2m'].max())
    min_temp = int(df['temperature_2m'].min())
    max_precip_prob = int(df['precipitation_probability'].max())
    time_of_max_precip = df.loc[df['precipitation_probability'].idxmax(
    )]['date']
    avg_cloud_cover = df['cloud_cover'].mean()
    current_temperature_2m = int(df["current_temperature_2m"].iloc[0])
    current_precipitation = df["current_precipitation"].iloc[0]
    current_apparent_temperature = int(
        df["current_apparent_temperature"].iloc[0])

    title_emoji = ""
    day_summary = ""
    if max_precip_prob > 40:
        title_emoji = "🌧️"
        day_summary = f"Heads up for rain, with the highest chance around {time_of_max_precip.strftime('%-I %p')}."
    elif avg_cloud_cover > 65:
        title_emoji = "☁️"
        day_summary = "It will be a mostly cloudy day."
    elif avg_cloud_cover < 30:
        title_emoji = "☀️"
        day_summary = "Expect plenty of sunshine."
    else:
        title_emoji = "⛅️"
        day_summary = "It will be partly cloudy."

    temp_high_emoji = "🥵" if max_temp > 28 else ""
    temp_low_emoji = "🥶" if min_temp < 5 else ""
    current_precip_emoji = "💧" if current_precipitation > 0 else ""

    morning_summary, morning_emoji = get_period_summary(df, 7, 12)
    afternoon_summary, afternoon_emoji = get_period_summary(df, 12, 18)
    evening_summary, evening_emoji = get_period_summary(df, 18, 23)

    message = f"""
    Weather on Buenos Aires for tomorrow {title_emoji}

    - Right Now: {current_temperature_2m}°C (feels like {current_apparent_temperature}°C) {current_precip_emoji}
    - High: {max_temp}°C {temp_high_emoji}
    - Low: {min_temp}°C {temp_low_emoji}
    - Summary: {day_summary}

    - {morning_emoji}  Morning: {morning_summary}.
    - {afternoon_emoji} Afternoon: {afternoon_summary}.
    - {evening_emoji}  Evening: {evening_summary}.

    """

    return message
