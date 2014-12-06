# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArticleType'
        db.create_table('core_articletype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['ArticleType'])

        # Adding model 'ArticleSubType'
        db.create_table('core_articlesubtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('article_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ArticleType'])),
        ))
        db.send_create_signal('core', ['ArticleSubType'])

        # Adding field 'Article.article_sub_type'
        db.add_column('core_article', 'article_sub_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['core.ArticleSubType']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ArticleType'
        db.delete_table('core_articletype')

        # Deleting model 'ArticleSubType'
        db.delete_table('core_articlesubtype')

        # Deleting field 'Article.article_sub_type'
        db.delete_column('core_article', 'article_sub_type_id')


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