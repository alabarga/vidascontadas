# coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import scrap.items as items

from bs4 import BeautifulSoup
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

        item = items.PeopleItem()
        item['url'] = response.url

        ficha = html.find('div', {'class':'ficha_desc'})

        re_born_date_year = re.search( u'A\xf1o: \d{4}', ficha.text,
                                       re.M|re.I|re.U)
        date_born_year = int(re.sub('A\xf1o: ', '', re_born_date_year.group()))\
                    if re_born_date_year else 0
        re_born_date_month = re.search( u'Mes: \d{1,2}', ficha.text,
                                       re.M|re.I|re.U)
        date_born_month = int(re.sub('Mes: ', '', re_born_date_month.group()))\
                    if re_born_date_month else 0
        re_born_date_day = re.search( u'D\xeda: \d{1,2}', ficha.text,
                                       re.M|re.I|re.U)
        date_born_day = int(re.sub('D\xeda: ', '', re_born_date_day.group()))\
                    if re_born_date_day else 0


        item.save()

        return item

