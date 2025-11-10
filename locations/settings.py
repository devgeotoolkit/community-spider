# -*- coding: utf-8 -*-
import os

BOT_NAME = 'locations'
LOG_LEVEL = "DEBUG"

SPIDER_MODULES = ['locations.spiders']
NEWSPIDER_MODULE = 'locations.spiders'

FEED_EXPORTERS = {
    'json': 'scrapy.exporters.JsonItemExporter',
    'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
    'jl': 'scrapy.exporters.JsonLinesItemExporter',
    'csv': 'scrapy.exporters.CsvItemExporter',
    'xml': 'scrapy.exporters.XmlItemExporter',
    'marshal': 'scrapy.exporters.MarshalItemExporter',
    'pickle': 'scrapy.exporters.PickleItemExporter',
    'geojson': 'locations.exporters.GeoJsonExporter',
    'ndgeojson': 'locations.exporters.LineDelimitedGeoJsonExporter',
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Linux; rv:1.0)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

FEED_URI = os.environ.get('FEED_URI')
FEED_FORMAT = os.environ.get('FEED_FORMAT')

FEED_EXPORT_ENCODING = 'utf-8'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': '*/*',
  'Accept-Language': 'en',
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'locations.extensions.LogStatsExtension': 101,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'locations.pipelines.DuplicatesPipeline': 200,
   'locations.pipelines.ApplySpiderNamePipeline': 250,
   'locations.pipelines.ApplySpiderLevelAttributesPipeline': 300,
}