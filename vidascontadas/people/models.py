#coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Relation(models.Model):
    relation = models.CharField(_('Relation'), null=True, blank=True,
                                max_length=50)
    person_1 = models.ForeignKey('people.People', related_name='relations_1')
    person_2 = models.ForeignKey('people.People', related_name='relations_2')

    class Meta:
        verbose_name = _('Relation')
        verbose_name_plural = _('Relations')

    def __unicode__(self):
        return u'%s, %s  %s' % (unicode(self.relation), unicode(self.person_1),
                                unicode(self.person_2))


class EventPeople(models.Model):
    role = models.CharField(_('Role'), null=True, blank=True,
                                max_length=50)
    people = models.ForeignKey('people.People')
    event = models.ForeignKey('events.Event')

    class Meta:
        verbose_name = _('Event people')
        verbose_name_plural = _('Events people')

    def __unicode__(self):
        return u'%s, %s  %s' % (unicode(self.role), unicode(self.people),
                                unicode(self.event))


class PoliticalActivity(models.Model):
    role = models.CharField(_('Role'), null=True, blank=True,
                                max_length=50)
    people = models.ForeignKey('people.People')
    affiliation = models.ForeignKey('politician.Affiliation')

    class Meta:
        verbose_name = _('Political Activity')
        verbose_name_plural = _('Political activities')

    def __unicode__(self):
        return u'%s, %s  %s' % (unicode(self.role), unicode(self.people),
                                unicode(self.affiliation))


class People(models.Model):
    GENRE_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female'),)

    name = models.CharField(_('Name'), null=False, blank=True, max_length=100)
    surname = models.CharField(_('Name'), null=False, blank=True,
                               max_length=100)
    genre = models.CharField(_('Genre'), null=False, choices=GENRE_CHOICES,
                                default=GENRE_CHOICES[0][0], max_length=2)
    profession = models.CharField(_('Profession'), null=False, blank=True,
                                  max_length=75)
    date_birth = models.DateTimeField(_('Date birth'), null=False, blank=True)
    date_death = models.DateTimeField(_('Date death'), null=False, blank=True)
    death_cause = models.CharField(_('Death cause'), null=False, blank=True,
                                   max_length=100)
    place_birth = models.ForeignKey('places.Place', related_name='place_births')
    place_death = models.ForeignKey('places.Place', related_name='place_deaths')
    burying_place = models.ForeignKey('places.Place',
                                      related_name='burying_places')
    address = models.ForeignKey('places.Place', related_name='addreses')
    married = models.BooleanField(_('Married'), null=False, blank=False,
                                  default=True)
    childrens = models.IntegerField(_('Childrens'), null=False, blank=True,
                                    default=0)
    references = models.ManyToManyField('references.Reference')
    medias = models.ManyToManyField('medias.Media')
    relations = models.ManyToManyField('people.People', through='people.Relation')
    events = models.ManyToManyField('events.Event', through='people.EventPeople')
    political_activities = models.ManyToManyField('politician.Affiliation', through='people.PoliticalActivity')


    class Meta:
        verbose_name = _('People')
        verbose_name_plural = _('People')

    def __unicode__(self):
        return u'%s, %s (%s-%s)' % (unicode(self.name), unicode(self.surname),
                            unicode(self.date_birth), unicode(self.date_death))
