#coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Media(models.Model):
    TYPE_CHOICES = (('image','Image'),
                    ('pdf', 'Pdf'),
                    ('video', 'Video'),
                    ('audio', 'Audio'))

    media_file = models.FileField(_('Media file'), upload_to='medias',
                                  null=False, blank=False)
    media_type = models.CharField(_('Media type'), max_length=50,
                                  choices=TYPE_CHOICES,
                                  default=TYPE_CHOICES[0][0])

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Medias')

    def __unicode__(self):
        return u'%s: %s' % (unicode(self.media_type), unicode(self.media_file))
