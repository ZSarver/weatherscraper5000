"""This module implements a web scraper for temperature history information."""

import datetime
import json
import re
import urllib

import requests
from bs4 import BeautifulSoup

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
        self.data = None
    def __str__(self):
        if self.data is None:
            self.parse()
        return str(self.data)

    def parse(self):
        html = BeautifulSoup(self.response.text, "html.parser")
        #check for errors
        #first check for a bad response
        if not self.response.ok:
            raise urllib.error.URLError("Bad HTTP response: " + str(self.response.status_code))
        #check for an ambiguous location
        ambi = html("p", class_="listHeading")
        if ambi:
            if ambi[0].string == "Select a location:":
                raise urllib.error.URLError("Ambiguous location given")
        #the first nine wx-values in the page are always the mean, max, and min temperatures
        temps = html("span", class_="wx-value")
        self.data = json.dumps(
            {
                "Mean Temperature": {
                    "Actual": temps[0].string + " °F",
                    "Average": temps[1].string + " °F"
                },
                "Max Temperature": {
                    "Actual": temps[2].string + " °F",
                    "Average": temps[3].string + " °F",
                    "Record": {
                        "Temperature": temps[4].string + " °F",
                        "Year": ""
                    }
                },
                "Min Temperature": {
                    "Actual": temps[5].string + " °F",
                    "Average": temps[6].string + " °F",
                    "Record": {
                        "Temperature": temps[7].string + " °F",
                        "Year": ""
                    }
                }
            }, indent=4
        )
