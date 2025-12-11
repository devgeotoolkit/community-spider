import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from locations.http import SeleniumRequest

class bbva_per_dpaSpider(scrapy.Spider):
    name = 'bbva_per_dpa'
    brand_name = 'BBVA'
    spider_type = 'chain'
    spider_chain_id = '1749'
    spider_categories = []
    spider_countries = [pycountry.countries.lookup('PER').alpha_3]
    allowed_domains = ["www.bbva.pe"]
    count = 0
    download_delay = 5
    name_counts = {}
    
    # start_urls = ["https://www.bbva.pe/"]
      
    def start_requests(self):
        st = "https://www.bbva.pe/personas/oficinas.pag-1.html"
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'referer': 'https://www.bbva.pe/personas/oficinas.html',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }
        yield SeleniumRequest(url=st, headers = headers,  callback=self.parse) 

    def parse(self, response):
        next_page = response.xpath('//article[@class="pagination__navlast"]/a[@class="pagination__navitem link__base "]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        branch_root = response.xpath('//div[@class="editorialcardgrid__cards"]/div/div/div/div[1]')
        for branch in branch_root:
            name = branch.xpath('.//div[@class="card__body rte"]/text()').get()
            location_name = name.replace('\n','').strip()

            # Check for duplicates and append a number if needed
            if location_name in self.name_counts:
                self.name_counts[location_name] += 1
                unique_name = f"{location_name} {self.name_counts[location_name]}"
            else:
                self.name_counts[location_name] = 1
                unique_name = location_name

            finalData = {}
            self.count += 1
            finalData['ref'] = str(self.count)
            finalData['chain_name'] = self.brand_name
            finalData['chain_id'] = self.spider_chain_id
            finalData['name'] =  unique_name 
            street = branch.xpath('.//div[@class="promocard__contactinfo rte"][1]/text()').get()
            finalData['street'] = street.replace('\n','').replace(' ','').replace('–','').strip()
            finalData['country'] = 'Peru'
            finalData['addr_full'] = f"{finalData['street']} {finalData['country']}"
            phone_numbers = branch.xpath('.//div[@class="promocard__contactinfo rte"][2]/text()').get()
            finalData['website'] = 'https://www.bbva.pe/'
            yield GeojsonPointItem(**finalData)
