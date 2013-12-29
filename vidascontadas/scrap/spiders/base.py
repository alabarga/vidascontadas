# coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import scrap.items as items
from common.models import CustomDate
from cities_light.models import City
from places.models import Place

from bs4 import BeautifulSoup

import re


def get_int_from_text(expression, sub, text):
    re_result = re.search(expression, text, re.M|re.I|re.U)
    return int(re.sub(sub, '', re_result.group())) if re_result else 0

def get_place_from_text(place_html):
    city_query = City.objects

    #region
    region_html = place_html.findNext(text=re.compile('Provincia: \w+'))
    region_text = re.sub('Provincia: ', '', region_html)
    if not region_text == u'No informa/Ez du informatzen':
        city_query = city_query.filter(region__name__iexact=region_text)
        if not city_query:
            pass
            #TODO
            #send mail with data to add to db

    #city
    city_html = place_html.find_next(text=re.compile('Municipio: \w+'))
    city_text = re.sub('Municipio: ', '', city_html)
    if not city_text == u'No informa/Ez du informatzen':
        city_query = city_query.filter(name__iexact=city_text)
        if not city_query:
            pass
            #TODO
            #send mail with data to add to db

    city = None
    if city_query != City.objects and city_query:
        if len(city_query) > 1:
            pass
            #TODO
            #send mail to detect duplication cities
        else:
            city = city_query[0]

    name = ''
    #neighbourhood
    neighbourhood_html = place_html.find_next(
                         text=re.compile('Concejo o barrio: \w+'))
    neighbourhood_text = re.sub('Concejo o barrio: ', '', neighbourhood_html)
    if not neighbourhood_text == u'No informa/Ez du informatzen':
        name += neighbourhood_text

    #subregion
    subregion_html = place_html.find_next(
                         text=re.compile('Comarca: \w+'))
    subregion_text = re.sub('Comarca: ', '', subregion_html)
    if not subregion_text == u'No informa/Ez du informatzen':
        name += subregion_text

    #get place
    places = Place.objects

    places = places.filter(city=city) if city else places.none()

    if name != '' or places:
        place, created = places.get_or_create(name=name)
        place.save()
        return place
    else:
        return None


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

        #birth places
        birth_place_html = ficha.find(text='Lugar de nacimiento')
        item['place_birth'] = get_place_from_text(birth_place_html)

        item.save()

        print item['place_birth']

        return item

