import scrapy
import re
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_links = response.css('a[href^="pep-"]')
        for pep_link in all_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_status = response.css('abbr::text').get()
        name_with_number = response.css('h1.page-title::text').get()
        name = name_with_number.split('– ')
        pattern = r'\d+'
        number = re.search(pattern, name_with_number)
        data = {
            'number': number[0],
            'name': name[1],
            'status': pep_status,
        }
        yield PepParseItem(data)
