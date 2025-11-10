import scrapy
import uuid
import pycountry
from locations.items import GeojsonPointItem
from urllib.parse import urlencode
from locations.categories import Code


class AralSpider(scrapy.Spider):
    name = "aral_lux_dpa"
    brand_name = "ARAL"
    spider_type = "chain"
    spider_chain_id = "6"
    spider_categories = [
        Code.PETROL_GASOLINE_STATION.value
    ]
    spider_countries = [
        pycountry.countries.lookup("LUX").alpha_3
    ]

    # start_urls = ["https://aral.de"]

    def start_requests(self):
        headers = {
            'authority': 'tankstellenfinder.aral.de',
            'accept': 'application/json, text/javascript',
            'accept-language': 'es-ES,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'ap-analytics=false; ap-marketing=false; ap-functional=true; logglytrackingsession=8ad498f6-091c-40c1-8f76-1bb5713b6ae0; ap-auth=Q2NXS0Q1bmVPSDRJTTdnSHNaejVrTzFFS3dnVGM2cUdjZDF2dGEvdUxsNWxoWEZCNFNHaGNVWkdEYWpiT2dNTW12eGkwL3dyS3pCcnVuQUxweG5CbkJXbGZoblhpZGVLdXovTnZHZnhZSHMxdGUvQkkyaVcwZDZNNU9QRGlJaC9zL1NEbzRkeDNVTT0%3D',
            'if-none-match': 'W/"159c4ee3d861a40deb98b6c79f3c7431"',
            'referer': 'https://tankstellenfinder.aral.de/?auth=7e73564d29',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }   

        lat_range = (49, 50)
        lng_range = (5, 7)
        lat_increment = 0.5
        lng_increment = 0.5

        lat_iterations = int((self.lat_range[1] - self.lat_range[0]) / self.lat_increment) + 1
        lng_iterations = int((self.lng_range[1] - self.lng_range[0]) / self.lng_increment) + 1

        unique_coordinates = set()

        for lat_iteration in range(lat_iterations):
            for lng_iteration in range(lng_iterations):
                lat = self.lat_range[0] + (self.lat_increment * lat_iteration)
                lng = self.lng_range[0] + (self.lng_increment * lng_iteration)

                params = {
                    'lat': str(lat),
                    'lng': str(lng),
                    'autoload': 'true',
                    'travel_mode': 'driving',
                    'avoid_tolls': 'false',
                    'avoid_highways': 'false',
                    'show_stations_on_route': 'true',
                    'corridor_radius': '5',
                    'format': 'json',
                }

                url = f'https://tankstellenfinder.aral.de/api/v1/locations/nearest_to?{urlencode(params)}'
                yield scrapy.Request(
                    url=url,
                    headers=self.headers,
                    callback=self.parse,
                    meta={'lat': lat, 'lng': lng, 'unique_coordinates': unique_coordinates}
                )

    def parse(self, response):
        lat = response.meta['lat']
        lng = response.meta['lng']
        unique_coordinates = response.meta['unique_coordinates']
        data = response.json()

        for item in data:
            lng = float(item["lng"])
            lat = float(item["lat"])
            country_code = item.get("country_code", "").upper()

            coordinates = (lat, lng)
            name_coordinates = (name, coordinates)

            if country_code == "LU" and name_coordinates not in unique_coordinates:
                unique_coordinates.add(name_coordinates)

                store_final = {
                    'ref': uuid.uuid4().hex,
                    'chain_name': self.brand_name,
                    'chain_id': self.spider_chain_id,
                    'street': item.get("address", ""),
                    'city': item.get('city', ''),
                    'store_url': item.get("website", ""),
                    'lat': lat,
                    'lon': lng,
                    'phone': item.get('telephone', ''),
                    'postcode': item.get('postcode', ''),
                    'opening_hours': item.get('opening_hours', '')
                }

                yield GeojsonPointItem(**store_final)
