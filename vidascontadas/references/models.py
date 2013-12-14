#coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Reference(models.Model):
    url = models.URLField(_('url'), null=False)
    contact = models.EmailField(_('Email'), null=False, blank=True)

    class Meta:
        verbose_name = _('Reference')
        verbose_name_plural = _('References')

    def __unicode__(self):
        return u'%s, %s' % (unicode(self.url), unicode(self.contact))
