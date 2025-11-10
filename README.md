# Project Community Spider - Places Data Engineering

Hi and welcome to the Community Spider.
Large companies, government organizations often add contact information on their own web resources so that clients can easily find the nearest office branches or service points.
The data can contain only address information without georeferencing, but in most cases, for the convenience of users, an interactive map is created with the display of objects in the form of points.

Our goal is to obtain data on the location of objects of a particular company with the maximum amount of related attributive information (phone number, work schedule, etc.).

## Project links
* Guideline: [Knowledge base](https://twilty.com/app/viewer/962ca15e-2e9c-4d40-910b-4fb381547ab0).

## User-facing deps
* Framework: Scrapy - [Scrapy Docs](https://scrapy.org/).
* Help packages:
    * BeautifulSoup - [bs4 docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).


## Installation
```bash
# install pipenv tool
pip install pipenv

# install dependencies
pipenv install

# run tests
pipenv run pytest

# run spider
pipenv run scrapy crawl {spider_name_dpa} -o {spider_name_dpa}.geojson --logfile={spider_name_dpa_error}.log -s LOGSTATS_FILE={spider_name_dpa_stats}.log 
```
