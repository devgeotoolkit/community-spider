from scrapy import spiderloader
from scrapy.utils import project
from urllib.parse import urlparse

settings = project.get_project_settings()
spider_loader = spiderloader.SpiderLoader.from_settings(settings)
spider_instances = [spider_loader.load(name) for name in spider_loader.list()]


class TestMetadata:
    # Spider Type
    def test_spider_type(self):
        for spider_instance in spider_instances:
            assert hasattr(
                spider_instance, "spider_type"), f"{spider_instance.name}, doesn't have spider_type attribute."

    def test_spider_type_values(self):
        for spider_instance in spider_instances:
            if hasattr(spider_instance, "spider_type"):
                assert spider_instance.spider_type == "chain" or spider_instance.spider_type == "generic", f"{spider_instance.name}, has wrong spider_type value. Possible values: chain, generic."

    # Brand Name
    def test_spider_brand_name(self):
        for spider_instance in spider_instances:
            if hasattr(spider_instance, "spider_type"):
                if spider_instance.spider_type == "chain":
                    assert hasattr(
                        spider_instance, "brand_name"), f"{spider_instance.name}, has spider_type=chain but doesn't have brand_name attribute."

    # Chain ID
    def test_spider_chain_id(self):
        for spider_instance in spider_instances:
            if spider_instance.spider_type == "chain":
                assert hasattr(
                    spider_instance, "spider_chain_id"), f"{spider_instance.name}, has spider_type=chain but doesn't have spider_chain_id attribute."

    
    def test_spider_chain_id_value(self):
        for spider_instance in spider_instances:
            if hasattr(spider_instance, "spider_chain_id"):
                assert type(spider_instance.spider_chain_id) == str, f"{spider_instance.name}, spider_chain_id should store only String data type."

    # Categories
    def test_spider_categories(self):
        for spider_instance in spider_instances:
            assert hasattr(spider_instance, "spider_categories"), f"{spider_instance.name}, doesn't have spider_categories attribute."


    def test_spider_categories_values(self):
        for spider_instance in spider_instances:
            if hasattr(spider_instance, "spider_categories"):
                assert all([type(category) == str for category in spider_instance.spider_categories]), f"{spider_instance.name}, spider_categories should store array of strings attribute."

    # Countries
    def test_spider_countries(self):
        for spider_instance in spider_instances:
            assert hasattr(spider_instance, "spider_countries"), f"{spider_instance.name}, doesn't have spider_countries attribute."

    def test_spider_countries_values(self):
        for spider_instance in spider_instances:
            if hasattr(spider_instance, "spider_countries"):
                assert all([type(country) == str for country in spider_instance.spider_countries]), f"{spider_instance.name}, spider_countries should store array of strings attribute."

    # Allowed domains
    def test_allowed_domains_values(self):
        for spider_instance in spider_instances:
            if hasattr(spider_instance, "allowed_domains"):
                assert all([type(domain) == str for domain in spider_instance.allowed_domains]), f"{spider_instance.name}, allowed_domains attribute should be in string format."

    # Start urls
    def test_starts_urls_values(self):
        for spider_instance in spider_instances:
            if hasattr(spider_instance, "start_urls"):
                checked_urls: list[bool] = []

                for url in spider_instance.start_urls:
                    if urlparse(url).scheme == 'https' or urlparse(url).scheme == 'http':
                        checked_urls.append(True)
                    else:
                        checked_urls.append(False)

                assert all(checked_urls), f"{spider_instance.name}, start_urls contains wrong urls."