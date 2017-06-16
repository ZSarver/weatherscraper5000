"""A module that tests weatherscraper5000"""

import unittest

import datetime
import json
import requests
from urllib import error

from weatherscraper5000 import WeatherScraper5000

class TestWeatherScraper5000(unittest.TestCase):
    def setUp(self):
        self.scraper = WeatherScraper5000("Atlanta, GA", datetime.date(1987, 5, 17))

    def test_exist(self):
        self.assertIsNotNone(self.scraper)

    def test_fetches_weather_history(self):
        self.assertTrue(self.scraper.response.ok)

    def test_error_on_ambiguous(self):
        bad = WeatherScraper5000("Atlanta", datetime.date(1987, 5, 17))
        self.assertRaises(error.URLError, bad.parse)

    def test_parses_weather_history(self):
        expected = json.dumps(
            {
                "Mean Temperature": {
                    "Actual": "72 °F",
                    "Average": "70 °F"
                    },
                "Max Temperature": {
                    "Actual": "82 °F",
                    "Average": "81 °F",
                    "Record": {
                        "Temperature": "90 °F",
                        "Year": "2001"
                        }
                    },
                "Min Temperature": {
                    "Actual": "62 °F",
                    "Average": "58 °F",
                    "Record": {
                        "Temperature": "43 °F",
                        "Year": "2014"
                        }
                    }
            }, indent=4)
        self.assertEqual(str(self.scraper), str(expected))

if __name__ == '__main__':
    unittest.main()
