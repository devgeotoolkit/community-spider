import scrapy
import pycountry
import json
from locations.categories import Code
from locations.items import GeojsonPointItem


class NinetyNinePancakeSpider(scrapy.Spider):
    name = '99_pancakes_ind_dpa'
    brand_name = "99 Pancakes"
    spider_type = "chain"
    spider_chain_id = "34184"
    spider_categories = []
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]

    # start_urls = ['https://www.99pancakes.in/index.php']

    def start_requests(self):

        form_data = {
            'shopData': "99-pancakes.myshopify.com"
        }

        url = 'https://storelocator.metizapps.com/stores/storeDataGet'

        yield scrapy.FormRequest(
            url=url,
            formdata=form_data,
            callback=self.parse
        )

    def parse(self, response):
        store_data = json.loads(response.text)

        for store in store_data['data']['result']:
            data = {
                'ref': store['id'],
                'chain_name': self.brand_name,
                'chain_id': self.spider_chain_id,
                'addr_full': store['address'],
                'city': store['cityname'],
                'state': store['statename'],
                'postcode': store['zipcode'],
                'country': store['countryname'],
                'phone': store['phone'],
                'website': 'https://99pancakes.in',
                'lat': store['mapLatitude'],
                'lon': store['mapLongitude'],
            }

            yield GeojsonPointItem(**data)
