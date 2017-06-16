"""The main function takes 4 command line parameters, constructs a WeatherScraper object,
    and pretty prints it to stdout"""

import argparse
import datetime

from weatherscraper5000 import WeatherScraper5000

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
    scraper = WeatherScraper5000.Scraper(args.location,
                                         datetime.date(args.year, args.month, args.day))
    print(scraper)

if __name__ == '__main__':
    main()