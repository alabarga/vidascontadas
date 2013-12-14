#coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Place(models.Model):
    city = models.ForeignKey('cities_light.City', null=False)
    name = models.CharField(_('Name'), max_length=100, null=False)
    place_type = models.CharField(_('Place type'), max_length=50, null=False,
                                  blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, null=False,
                                   blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, null=False,
                                   blank=True)

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')

    def __unicode__(self):
        return u'%s: %s' % (unicode(self.name), unicode(self.city))
