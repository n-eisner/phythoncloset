# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recommended'
        db.create_table('core_recommended', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('rec_for', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Article'])),
        ))
        db.send_create_signal('core', ['Recommended'])


    def backwards(self, orm):
        # Deleting model 'Recommended'
        db.delete_table('core_recommended')


    models = {
        'core.article': {
            'Meta': {'object_name': 'Article'},
            'article_sub_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ArticleSubType']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'core.articlesubtype': {
            'Meta': {'object_name': 'ArticleSubType'},
            'article_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ArticleType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'core.articletype': {
            'Meta': {'object_name': 'ArticleType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'core.recommended': {
            'Meta': {'object_name': 'Recommended'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'rec_for': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Article']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']