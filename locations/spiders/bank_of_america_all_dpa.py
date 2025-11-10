
# -*- coding: utf-8 -*-

import scrapy
import pycountry
import uuid
from locations.categories import Code
from locations.items import GeojsonPointItem
import re


class BankofAmericaSpider(scrapy.Spider):    
    name = "bank_of_america_all_dpa"
    brand_name = "Bank of America"
    spider_type = "chain"
    spider_chain_id = "1290"
    spider_categories = [Code.BANK.value]
    spider_countries = ["ALL"]

    # start_urls = ["https://www.bankofamerica.com/"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://business.bofa.com/content/boaml/en_us/locations.html",
            method="GET",
            callback=self.parse,
        )

    def parse(self, response):
        for container in response.css('.aem-wrap--layout-container'):
            header_text = container.css('h2.header__headline::text').get()
            if header_text:
                addresses = container.css('.aem-wrap--text')
                for address in addresses:
                    text = address.css('a::text').get(default='').strip()
                    if "Go to" in text:
                        continue
                    else:
                        address_text = address.css('p b::text').get()
                        if address_text:
                            if '|' in address_text:
                                city = address_text.split('|')[0].strip()
                            else:
                                city = address_text.strip()
                        else:
                            continue
                        
                        full_address = address.css('p::text').getall()
                        phone_numbers = []
                        for p_tag in address.css('p'):
                            if "Fax:" not in p_tag.get():
                                phones = p_tag.css('a[href^="tel:"]::text').getall()
                                phone_numbers.extend([number.strip() for number in phones])

                        full_address = [item for item in full_address if 'Tel:' not in item and 'Fax:' not in item]
                        selected_phone = phone_numbers[0] if phone_numbers else None
                        if ',' in city:
                            city_name, country = [part.strip() for part in city.rsplit(',', 1)]
                        else:
                            city_name = city
                            country = "United States"

                        mappedAttributes = {
                            'chain_name': self.brand_name,
                            'chain_id': self.spider_chain_id,
                            'ref': uuid.uuid4().hex,
                            'addr_full': ', '.join(full_address).strip(),
                            'city': city_name,
                            'country': country,
                            'phone': selected_phone,
                            'website': "https://business.bofa.com/content/boaml/en_us/locations.html"
                        }

                        yield GeojsonPointItem(**mappedAttributes)
