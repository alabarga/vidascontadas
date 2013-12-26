# coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import scrap.items as items
from common.models import CustomDate

from bs4 import BeautifulSoup

import re


class UnavarraSpider(CrawlSpider):
    name = 'unavarra'
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

        #name
        item['name'] = ficha.find('h2').text

        #genre
        genre_html = ficha.find('p', 't1').next_element
        item['genre'] = 'F' if genre_html == 'Mujer'\
                        else 'M' if genre_html == 'Hombre'\
                        else 'U'

        #birth date
        re_birth_date_year = re.search( u'A\xf1o: \d{4}', ficha.text,
                                       re.M|re.I|re.U)
        date_birth_year = int(re.sub('A\xf1o: ', '', re_birth_date_year.group()))\
                    if re_birth_date_year else 0
        re_birth_date_month = re.search( u'Mes: \d{1,2}', ficha.text,
                                       re.M|re.I|re.U)
        date_birth_month = int(re.sub('Mes: ', '', re_birth_date_month.group()))\
                    if re_birth_date_month else 0
        re_birth_date_day = re.search( u'D\xeda: \d{1,2}', ficha.text,
                                       re.M|re.I|re.U)
        date_birth_day = int(re.sub('D\xeda: ', '', re_birth_date_day.group()))\
                    if re_birth_date_day else 0

        date_birth, created = CustomDate.objects.get_or_create(
                               year=date_birth_year,
                               month=date_birth_month,
                               day=date_birth_day)
        date_birth.save()
        item['date_birth'] = date_birth

        item.save()

        print item.fields

        return item

