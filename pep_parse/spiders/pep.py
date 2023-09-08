import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_links = response.css('a[href^="pep-"]')
        for pep_link in all_links:
            pattern = r'pep-\d+'
            link_str = pep_link.css('a').get()
            link = re.search(pattern, link_str)
            yield response.follow(link[0] + '/', callback=self.parse_pep)

    def parse_pep(self, response):
        pep_status = response.css('dt:contains("Status:") + dd')
        name_with_number = response.css('h1.page-title::text').get()
        pattern = r'(?P<number>\d+) – (?P<name>.*)'
        number = re.search(pattern, name_with_number)
        number, name = number.groups()
        data = {
            'number': number,
            'name': name,
            'status': pep_status.css("abbr::text").get(),
        }
        yield PepParseItem(data)
