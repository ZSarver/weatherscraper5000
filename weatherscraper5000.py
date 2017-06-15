"""This module implements a web scraper for temperature history information."""

import datetime
import requests

class WeatherScraper5000:
    """Parse and format weather data from Weather Underground."""
    def __init__(self, location: str, date: datetime.date):
        self.params = {
            "airportorwmo": "query",
            "historytype": "DailyHistory",
            "backurl": "/history/index.html",
            "code": location,
            "month": date.month,
            "day": date.day,
            "year": date.year
        }
        self.response = requests.get("https://www.wunderground.com/cgi-bin/findweather/getForecast",
                                     params=self.params)
        