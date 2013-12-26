# coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.contrib.djangoitem import DjangoItem

import people.models as people


class PeopleItem(DjangoItem):
    django_model = people.People

    def save(self, commit=True):
        _saved_obj = self.django_model.objects.filter(
            url=self['url']).values_list(
                'id', flat=True)
        modelargs = dict((k, self.get(k)) for k in self._values
                         if k in self._model_fields)
        model = self.django_model(**modelargs)
        model.pk = _saved_obj[0] if _saved_obj else \
            self.django_model._meta.pk.get_default()
        if commit:
            model.save()
        return model
