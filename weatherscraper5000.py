"""This module implements a web scraper for temperature history information."""

import argparse
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
        self.date = date
        self.response = requests.get("https://www.wunderground.com/cgi-bin/findweather/getForecast",
                                     params=self.params)
        self.data = None
    def __str__(self):
        if self.data is None:
            self.parse()
        return str(self.data)

    def parse(self):
        """This method parses the response to produce a json object"""
        #first make sure the date is valid
        if self.date > datetime.date.today() or self.date < datetime.date(1947, 1, 1):
            raise ValueError("Given date is outside of history range.")
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

def main():
    """The main function takes 4 command line parameters, constructs a WeatherScraper object,
    and pretty prints it to stdout"""
    parser = argparse.ArgumentParser(description="Fetches temperature history.")
    parser.add_argument(
        'location',
        help="the location to find temperature history; be sure to quote any spaces!")
    maxyear = datetime.date.today().year + 1
    parser.add_argument('year', type=int, choices=range(1947, maxyear),
                        help="the year to find temperature history")
    parser.add_argument('month', type=int, choices=range(1, 13),
                        help="the month to find temperature history")
    parser.add_argument('day', type=int, choices=range(1, 32),
                        help="the day to find temperature history")
    args = parser.parse_args()
    scraper = WeatherScraper5000(args.location, datetime.date(args.year, args.month, args.day))
    print(scraper)

if __name__ == '__main__':
    main()
