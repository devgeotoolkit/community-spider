### This cocument provides example how to provide Fuel Types to GeoJSONPointItem model

```
from locations.attributes import FuelTypesEnum
from locations.models import ServicesModel

fuel_types = [FuelTypesEnum.Octane_100, FuelTypesEnum.Octane_89]
services = ServicesModel(FuelTypes=fuel_types)

mappedAttributes = {
    "ref": uuid.uuid4().hex,
    ...
    ...
    "services": services,
}

yield GeojsonPointItem(**mappedAttributes)            

```


#### Complete script example with mocked data

```
import scrapy
import pycountry
import re
from locations.categories import Code
from locations.attributes import FuelTypesEnum
from locations.models import ServicesModel
from locations.items import GeojsonPointItem
from typing import List
import uuid

EXTERNAL_DATA = [
    {
        "ref": "1",
        "chain_name": "Shell",
        "chain_id": "SHELL001",
        "name": "Shell Fuel Station Main Street",
        "phone": "+1 402-555-0123",
        "street": "123 Main Street",
        "country": "USA",
        "addr_full": "123 Main Street USA",
        "lat": 41.2565,
        "lon": -95.9345,
        "opening_hours": "Mo-Su 00:00-24:00",
        "store_url": "https://shell.example.com/station/123-main-st",
        "website": "https://www.shell.us/",
        "tags": {
            "amenity:fuel": "yes",
            "fuel:octane_87": "yes",
            "fuel:octane_89": "yes",
            "fuel:octane_91": "yes",
            "fuel:diesel": "yes",
            "fuel:propane": "no",
            "fuel:top_tier": "yes",
            "shop": "convenience",
            "brand:wikidata": "Q123456789"
        }
    },
    {
        "ref": "2",
        "chain_name": "Clean Energy",
        "chain_id": "CLEAN001",
        "name": "Clean Energy CNG Station Lincoln",
        "phone": "+1 402-555-0456",
        "street": "789 Greenway Blvd",
        "country": "USA",
        "addr_full": "789 Greenway Blvd USA",
        "lat": 40.8136,
        "lon": -96.7026,
        "opening_hours": "Mo-Fr 06:00-22:00; Sa-Su 08:00-20:00",
        "store_url": "https://cleanenergyfuels.com/station/lincoln",
        "website": "https://cleanenergyfuels.com/",
        "tags": {
            "amenity:fuel": "yes",
            "fuel:cng": "yes",
            "fuel:lng": "yes",
            "fuel:diesel": "no",
            "fuel:octane_87": "no",
            "fuel:octane_91": "no",
            "fuel:propane": "no",
            "fuel:top_tier": "no",
            "shop": "convenience",
            "brand:wikidata": "Q987654321"
        }
    },
]

class FuelTypesSpider(scrapy.Spider):
    name = "fuel_types_spider_dpa"
    brand_name = "Some Oil Company"
    spider_type = "chain"
    spider_chain_id = "none"
    spider_categories = [Code.PETROL_GASOLINE_STATION.value]
    spider_countries = [pycountry.countries.lookup("USA").alpha_3]
    
    start_urls = ["https://lukoil.com"]

    def parse(self, response):
        response = EXTERNAL_DATA
        
        for item in response:
            fuel_types = self.__map_tags_to_fuel_types(item['tags'])
            services = ServicesModel(FuelTypes=fuel_types)
            
            mappedAttributes = {
                "ref": uuid.uuid4().hex,
                "chain_name": item["chain_name"],
                "chain_id": item["chain_id"],
                "addr_full": item["addr_full"],
                "opening_hours": item["opening_hours"],
                "website": item["website"],
                "store_url": item["store_url"],
                "country": item["country"],
                "services": services,
            }
            yield GeojsonPointItem(**mappedAttributes)
    
    def __map_tags_to_fuel_types(self, tags: dict):
        mapping = {
            "fuel:octane_87": FuelTypesEnum.Octane_87,
            "fuel:octane_89": FuelTypesEnum.Octane_89,
            "fuel:octane_91": FuelTypesEnum.Octane_91,
            "fuel:diesel": FuelTypesEnum.Diesel,
            "fuel:propane": FuelTypesEnum.LPG,
            "fuel:cng": FuelTypesEnum.CNG,
            "fuel:lng": FuelTypesEnum.LNG,
        }

        fuel_types = []
        for key, value in tags.items():
            if value == "yes" and key in mapping:
                fuel_types.append(mapping[key])
        
        return fuel_types
```