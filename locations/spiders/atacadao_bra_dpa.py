import scrapy
import json
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code

class Atacadao_bra_dpaSpider(scrapy.Spider): 
    name = 'atacadao_bra_dpa'
    brand_name = 'Atacadão'
    spider_type = 'chain'
    spider_chain_id = '23667'
    spider_categories = [Code.GROCERY.value]
    spider_countries = [pycountry.countries.lookup('BRA').alpha_3]
    
    # start_urls = ["https://www.atacadao.com.br/"]

    def start_requests(self):
        states = ["AC",	"AL",	"AP",	"AM",	"BA",	"CE",	"DF",	"ES",	"GO",	"MA",	"MT",	"MS",	"MG",	"PA",	"PB",	"PR",	"PE",	"PI",	"RJ",	"RN",	"RS",	"RO",	"RR",	"SC",	"SP",	"SE"]
        st = "https://apihub.carrefour.com.br/br-atc-api-middleware-flyer-services/v2/store/city?uf={}&city=&PageSize=1000&pageNumber=1"

        headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.atacadao.com.br',
                'priority': 'u=1, i',
                'referer': 'https://www.atacadao.com.br/institucional/nossas-lojas',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            }
        for state in states:
            url = st.format(state)  
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers=headers
            )

    def parse(self, response):
        Stores = response.json() 
         
        for Store in Stores.get("stores",[]):
            
            finalData = {}
            finalData['ref'] = Store.get('storeId', '')
            finalData['chain_name'] = self.brand_name
            finalData['chain_id'] = self.spider_chain_id
            name = Store.get('loja', '')
            finalData["name"] = f"Atacadão {name}"
            street1 = Store.get('endereco', '') 
            street2 = Store.get('numero', '')
            street3 = Store.get('bairro', '')
            finalData["street"] = f'{street1} {street2} {street3}'.replace("’",'')
            finalData["city"] = Store.get('cidade', '')
            finalData["state"] = Store.get('estado', '')
            finalData["postcode"] = Store.get('cep', '')
            finalData['lat'] = Store.get('lat', 0.0)
            finalData['lon'] = Store.get('long', 0.0) 
            finalData["phone"] = Store.get('telefone', '')
            opening_hours = self.parse_opening_hours(Store)
            finalData["opening_hours"] = opening_hours
            finalData['website'] = "https://www.atacadao.com.br/"
            
            yield GeojsonPointItem(**finalData)

    def parse_opening_hours(self, Store):
        opening_hours = []

        segSabAbre = Store.get("segSabAbre", "")
        segSabFecha = Store.get("segSabFecha", "")
        domingoAbre = Store.get("domingoAbre", "")
        domingoFecha = Store.get("domingoFecha", "")

        if segSabAbre and segSabFecha:
            opening_hours.append(f"Mo - Sa {segSabAbre[:5]}-{segSabFecha[:5]}")
        if domingoAbre and domingoFecha:
            opening_hours.append(f"Su {domingoAbre[:5]}-{domingoFecha[:5]}")

        return "; ".join(opening_hours)
   