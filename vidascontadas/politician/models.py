#coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Affiliation(models.Model):
    name = models.CharField(_('name'), null=False, blank=True, max_length=75)

    class Meta:
        verbose_name = _('Affiliation')
        verbose_name_plural = _('Affiliations')

    def __unicode__(self):
        return u'%s' % (unicode(self.name))
