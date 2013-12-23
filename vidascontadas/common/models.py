#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomDate(models.Model):
    year = models.IntegerField(_('Year'), null=False, blank=True,
                               default=0)
    month = models.IntegerField(_('Month'), null=False, blank=True,
                                default=0)
    day = models.IntegerField(_('Day'), null=False, blank=True,
                              default=0)

    class Meta:
        verbose_name = _('Custom date')
        verbose_name_plural = _('Custom dates')

    def __unicode__(self):
        return u'%d/%d/%d' % (self.year, self.month, self.day)
