from setuptools import setup, find_packages

setup(
    name="WeatherScraper5000",
    version="0.0.1",
    packages=find_packages(),
    description="It scrapes the weather better than WeatherScraper4000",
    author="Zachary Sarver",
    author_email="Zachary.Sarver@gmail.com",
    license="GNU GPL v3",
    entry_points={
        "console_scripts": ["whistory = weatherscraper5000.main"]
    }
)