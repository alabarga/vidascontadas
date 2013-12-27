# coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import scrap.items as items
from common.models import CustomDate

from bs4 import BeautifulSoup

import re


def get_int_from_text(expression, sub, text):
    re_result = re.search(expression, text, re.M|re.I|re.U)
    return int(re.sub(sub, '', re_result.group())) if re_result else 0


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
        date_birth, created = CustomDate.objects.get_or_create(
                 year=get_int_from_text(u'A\xf1o: \d{4}','A\xf1o: ',ficha.text),
                 month=get_int_from_text(u'Mes: \d{4}','Mes: ',ficha.text),
                 day=get_int_from_text(u'D\xeda: \d{4}','D\xeda: ',ficha.text))
        date_birth.save()
        item['date_birth'] = date_birth

        #Age
        item['age'] = get_int_from_text(u'Edad: \d{1,3}','Edad: ',ficha.text)

        import ipdb;ipdb.set_trace()

        item.save()

        print item.fields

        return item

