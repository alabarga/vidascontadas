# coding=utf-8
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from bs4 import BeautifulSoup
import datetime
import re


class BaseSpider(CrawlSpider):
    name = 'base'
    allowed_domains = ['memoria-oroimena.unavarra.es', ]

    start_urls = [
            'http://memoria-oroimena.unavarra.es/es/buscar/?pax=1', ]

    def location_href_value(value):
        m = re.search("location.href=\'(.*)\'", value)

        return m.groups()[0]

    rules = [
        Rule(SgmlLinkExtractor(
            allow=['/es/buscar/\?pax=\d+'], unique=True), follow=True),
        Rule(SgmlLinkExtractor(
            allow=['.*'], tags=('div'), attrs=('onclick'), unique=True,
            process_value=location_href_value), 'parse_item'),]

    def parse_item(self, response):
        html = BeautifulSoup(response.body)
        ficha = html.find('div', {'class':'ficha_desc'})
        import ipdb;ipdb.set_trace()
        re_born_date = re.search( u'A\xf1o: \d{4}', ficha.text, re.M|re.I|re.U)
        date_born = int(re.sub('A\xf1o: ', '', re_born_date.group()))\
                    if re_born_date else 0

        print response.url

        return None

