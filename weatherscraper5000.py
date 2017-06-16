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
        """This method parses the response to produce a json object"""
        html = BeautifulSoup(self.response.text, "html.parser")
        #check for errors
        #first check for a bad response
        if not self.response.ok:
            raise urllib.error.URLError("Bad HTTP response: " + str(self.response.status_code))
        #check for an ambiguous location
        ambi = html("p", class_="listHeading")
        if ambi:
            raise urllib.error.URLError("Ambiguous location given")
        #check for nonexistant location
        bad = html("p", class_="airport-not-found")
        if bad:
            raise urllib.error.URLError("Entered location doesn't exist")
        #the first nine wx-values in the page are always the mean, max, and min temperatures
        temps = html("span", class_="wx-value")
        #the first two (####) numbers are record setting years
        entries = html("td")
        yearregex = re.compile("\(\d+\)")
        years = []
        for entry in entries:
            year = yearregex.search(str(entry))
            #each year is a regex match object, which means we can get the
            #content of the match (with parentheses stripped) with year[0][1:5]
            if year:
                years.append(year)
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
                        "Year": years[0][0][1:5]
                    }
                },
                "Min Temperature": {
                    "Actual": temps[5].string + " °F",
                    "Average": temps[6].string + " °F",
                    "Record": {
                        "Temperature": temps[7].string + " °F",
                        "Year": years[1][0][1:5]
                    }
                }
            }, indent=4
        )
