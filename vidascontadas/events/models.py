#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    event_date = models.DateTimeField(_('Event date'), null=False, blank=True)
    name = models.CharField(_('Name'), null=True, blank=True, max_length=50)
    description = models.TextField(_('Description'), null=False, blank=True)
    place = models.ForeignKey('places.Place')
    media = models.ManyToManyField('medias.Media')

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __unicode__(self):
        return u'(%s), %s' % (unicode(self.event_date), unicode(self.name))
