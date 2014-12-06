# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "web/core/fixtures/article_types.json")

    def backwards(self, orm):
        "Write your backwards methods here."

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
        'core.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']
    symmetrical = True
