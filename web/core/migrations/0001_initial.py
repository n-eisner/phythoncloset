# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('core_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['Tag'])

        # Adding model 'Article'
        db.create_table('core_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Article'])

        # Adding M2M table for field tags on 'Article'
        db.create_table('core_article_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['core.article'], null=False)),
            ('tag', models.ForeignKey(orm['core.tag'], null=False))
        ))
        db.create_unique('core_article_tags', ['article_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('core_tag')

        # Deleting model 'Article'
        db.delete_table('core_article')

        # Removing M2M table for field tags on 'Article'
        db.delete_table('core_article_tags')


    models = {
        'core.article': {
            'Meta': {'object_name': 'Article'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'core.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']