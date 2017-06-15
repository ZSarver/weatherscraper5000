"""A module that tests weatherscraper5000"""

import unittest

import datetime
import requests

from weatherscraper5000 import WeatherScraper5000

class TestWeatherScraper5000(unittest.TestCase):
    def setUp(self):
        self.scraper = WeatherScraper5000("Atlanta", datetime.date(1987, 5, 17))

    def test_exist(self):
        self.assertIsNotNone(self.scraper)

    def test_fetches_weather_history(self):
        self.assertEqual(self.scraper.response.status_code, requests.codes.ok)

if __name__ == '__main__':
    unittest.main()
