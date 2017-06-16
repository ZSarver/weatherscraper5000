"""A module that tests weatherscraper5000"""

import unittest

import datetime
import json
import subprocess
from urllib import error

from weatherscraper5000 import WeatherScraper5000

class TestWeatherScraper5000(unittest.TestCase):
    def setUp(self):
        self.scraper = WeatherScraper5000("Atlanta, GA", datetime.date(1987, 5, 17))
        self.maxDiff = 700

    def test_exist(self):
        self.assertIsNotNone(self.scraper)

    def test_fetches_weather_history(self):
        self.assertTrue(self.scraper.response.ok)

    def test_error_on_ambiguous(self):
        bad = WeatherScraper5000("Atlanta", datetime.date(1987, 5, 17))
        self.assertRaises(error.URLError, bad.parse)

    def test_error_on_nonexistant(self):
        bad = WeatherScraper5000("fadsf876dsfgae", datetime.date(1987, 5, 17))
        self.assertRaises(error.URLError, bad.parse)

    def test_bad_date_future(self):
        bad = WeatherScraper5000("Atlanta, GA", datetime.date(2525, 5, 17))
        self.assertRaises(ValueError, bad.parse)

    def test_bad_date_past(self):
        bad = WeatherScraper5000("Atlanta, GA", datetime.date(1900, 5, 17))
        self.assertRaises(ValueError, bad.parse)

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

    def test_main_success(self):
        result = subprocess.run('python ./weatherscraper5000.py "atlanta, ga" 1987 5 17')
        self.assertEqual(result.returncode, 0)

    def test_main_fail(self):
        result = subprocess.run('python ./weatherscraper5000.py "atlanta, ga" 1234 5 6')
        self.assertNotEqual(result.returncode, 0)
            
if __name__ == '__main__':
    unittest.main()
