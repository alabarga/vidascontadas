# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'People'
        db.create_table(u'people_people', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('genre', self.gf('django.db.models.fields.CharField')(default='M', max_length=2)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('date_birth', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('date_death', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('death_cause', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('place_birth', self.gf('django.db.models.fields.related.ForeignKey')(related_name='place_births', to=orm['places.Place'])),
            ('place_death', self.gf('django.db.models.fields.related.ForeignKey')(related_name='place_deaths', to=orm['places.Place'])),
            ('burying_place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='burying_places', to=orm['places.Place'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(related_name='addreses', to=orm['places.Place'])),
            ('married', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('childrens', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'people', ['People'])

        # Adding M2M table for field references on 'People'
        m2m_table_name = db.shorten_name(u'people_people_references')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('people', models.ForeignKey(orm[u'people.people'], null=False)),
            ('reference', models.ForeignKey(orm[u'references.reference'], null=False))
        ))
        db.create_unique(m2m_table_name, ['people_id', 'reference_id'])

        # Adding M2M table for field medias on 'People'
        m2m_table_name = db.shorten_name(u'people_people_medias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('people', models.ForeignKey(orm[u'people.people'], null=False)),
            ('media', models.ForeignKey(orm[u'medias.media'], null=False))
        ))
        db.create_unique(m2m_table_name, ['people_id', 'media_id'])


    def backwards(self, orm):
        # Deleting model 'People'
        db.delete_table(u'people_people')

        # Removing M2M table for field references on 'People'
        db.delete_table(db.shorten_name(u'people_people_references'))

        # Removing M2M table for field medias on 'People'
        db.delete_table(db.shorten_name(u'people_people_medias'))


    models = {
        u'cities_light.city': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('region', 'name'),)", 'object_name': 'City'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'feature_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'population': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Region']", 'null': 'True', 'blank': 'True'}),
            'search_names': ('cities_light.models.ToSearchTextField', [], {'default': "''", 'max_length': '4000', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'cities_light.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'code2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"}),
            'tld': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'blank': 'True'})
        },
        u'cities_light.region': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('country', 'name'),)", 'object_name': 'Region'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geoname_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'medias.media': {
            'Meta': {'object_name': 'Media'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'media_type': ('django.db.models.fields.CharField', [], {'default': "'image'", 'max_length': '50'})
        },
        u'people.people': {
            'Meta': {'object_name': 'People'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addreses'", 'to': u"orm['places.Place']"}),
            'burying_place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'burying_places'", 'to': u"orm['places.Place']"}),
            'childrens': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'date_birth': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_death': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'death_cause': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'married': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'medias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['medias.Media']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'place_birth': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'place_births'", 'to': u"orm['places.Place']"}),
            'place_death': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'place_deaths'", 'to': u"orm['places.Place']"}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['references.Reference']", 'symmetrical': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'places.place': {
            'Meta': {'object_name': 'Place'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'medias': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['medias.Media']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'place_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'references.reference': {
            'Meta': {'object_name': 'Reference'},
            'contact': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['people']