from setuptools import setup, find_packages

setup(
    name="WeatherScraper5000",
    version="0.0.1",
    packages=find_packages(exclude=["test_*"]),
    description="It scrapes the weather better than WeatherScraper4000",
    author="Zachary Sarver",
    author_email="Zachary.Sarver@gmail.com",
    license="GNU GPL v3",
    entry_points={
    },
    install_requires=["beautifulsoup4>=4.6.0", "requests>=2.18.1"]
)